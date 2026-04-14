from django.urls import path
from .views import home, UserListCreate, SongListCreate
from .views import register, login_view, logout_view
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('users/', UserListCreate.as_view(), name='user-list-create'),
    path('songs/api/', SongListCreate.as_view(), name='song-list-create'),  # Changed to avoid conflict
    path('songs/', views.song_list, name='song_list'),
    path('songs/add/', views.add_song, name='add_song'),
    path('songs/edit/<int:song_id>/', views.edit_song, name='edit_song'),
    path('songs/delete/<int:song_id>/', views.delete_song, name='delete_song'),
    path('api/songs/', views.get_songs, name='get_songs'),
    path('api/add_song/', views.add_song_ajax, name='add_song_ajax'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('blog/', views.blog_home, name='blog_home'),
    path('blog/new/', views.create_post, name='create_post'),
    path('blog/post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('notes/', views.private_notes, name='private_notes'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

]
