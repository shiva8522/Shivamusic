from django import forms
from .models import Song, Album, Artist, UserPlaylist
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

from django import forms
from .models import BlogPost, Comment, PrivateNote

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class PrivateNoteForm(forms.ModelForm):
    class Meta:
        model = PrivateNote
        fields = ['content']

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'album', 'duration', 'file']

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'artist', 'release_date']  # Fixed field name

class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['name', 'genre', 'bio']  # Added missing fields

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = UserPlaylist
        fields = ['name', 'songs']

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    address = forms.CharField(widget=forms.Textarea, required=False)
    is_admin = forms.BooleanField(
        required=False,
        label='Register as admin (requires admin approval)'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                phone_number=self.cleaned_data['phone_number'],
                address=self.cleaned_data['address'],
                is_admin=self.cleaned_data['is_admin']
            )
        return user