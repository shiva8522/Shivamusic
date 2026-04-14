from django.shortcuts import redirect, get_object_or_404
from .models import Song, Album, Artist, UserPlaylist
from .forms import SongForm, AlbumForm, ArtistForm, PlaylistForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test
import json
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm

# Create your views here.
from rest_framework import generics
from .models import User, Song
from .serializers import UserSerializer, SongSerializer
from django.shortcuts import render, redirect, get_object_or_404
from .models import BlogPost, Comment, PrivateNote
from .forms import BlogPostForm, CommentForm, PrivateNoteForm
from django.contrib.auth.decorators import login_required

def blog_home(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'music/blog_home.html', {'posts': posts})

from django.contrib.auth.decorators import user_passes_test

def admin_check(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.is_admin

@login_required
def admin_dashboard(request):
    if not request.user.userprofile.is_admin:
        return redirect('home')
    
    # Admin-only content
    users = User.objects.all()
    songs = Song.objects.all()
    
    return render(request, 'music/admin_dashboard.html', {
        'users': users,
        'songs': songs
    })

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    comments = post.comments.all().order_by('-created_at')
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.commenter = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        comment_form = CommentForm()
    return render(request, 'music/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog_home')
    else:
        form = BlogPostForm()
    return render(request, 'music/create_post.html', {'form': form})

@login_required
def private_notes(request):
    notes = PrivateNote.objects.filter(user=request.user).order_by('-created_at')
    if request.method == 'POST':
        form = PrivateNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('private_notes')
    else:
        form = PrivateNoteForm()
    return render(request, 'music/private_notes.html', {'notes': notes, 'form': form})


class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SongListCreate(generics.ListCreateAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer


@csrf_exempt
def add_song_ajax(request):
    """Handles AJAX POST request to add a song"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            title = data.get("title")
            album_id = data.get("album_id")

            if not title:
                return JsonResponse({"error": "Title is required"}, status=400)

            album = Album.objects.get(id=album_id) if album_id else None
            song = Song.objects.create(title=title, album=album)
            return JsonResponse({"message": "Song added successfully!", "song": {"id": song.id, "title": song.title}}, status=201)

        except Album.DoesNotExist:
            return JsonResponse({"error": "Invalid album ID"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)

# 🆕 Create
def add_song(request):
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Song uploaded successfully!")
            return redirect('song_list')
        else:
            print("Form errors:", form.errors)  # Debugging line
    else:
        form = SongForm()
    
    return render(request, 'music/add_song.html', {'form': form})

# 🔄 Update
def edit_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    if request.method == "POST":
        form = SongForm(request.POST, request.FILES, instance=song)
        if form.is_valid():
            form.save()
            return redirect('song_list')
    else:
        form = SongForm(instance=song)
    return render(request, 'music/song_form.html', {'form': form})

# ❌ Delete
def delete_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    if request.method == "POST":
        song.delete()
        return redirect('song_list')
    return render(request, 'music/song_confirm_delete.html', {'song': song})

# 📜 Read (List of Songs)
def song_list(request):
    songs = Song.objects.all()
    return render(request, 'music/song_list.html', {'songs': songs})

def get_songs(request):
    """Returns a list of songs in JSON format"""
    songs = list(Song.objects.values('id', 'title', 'album__title'))
    return JsonResponse({'songs': songs})

from django.shortcuts import render
from .models import Album

def add_song_page(request):
    """Render the add_song.html page"""
    albums = Album.objects.all()  # Fetch albums for dropdown
    return render(request, 'music/add_song.html', {'albums': albums})


# User Registration View
def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! You are now logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

# User Login View
# User Login View
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Check if user is admin
            try:
                profile = user.userprofile
                if profile.is_admin:
                    messages.success(request, "Admin login successful!")
                    return redirect("admin_dashboard")  # Create this view
                else:
                    messages.success(request, "Login successful!")
                    return redirect("home")
            except UserProfile.DoesNotExist:
                messages.error(request, "User profile not found.")
                return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

# User Logout View
def logout_view(request):
    logout(request)
    return redirect("home")

def home(request):
    return render(request, 'music/index.html')

