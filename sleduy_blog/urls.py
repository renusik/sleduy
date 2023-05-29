from django.urls import path
from .views import (
    PostListView,
    postDetailView,
    postCreateView,
    PostUpdateView,
    PostDeleteView,
	UserPostListView,
    random_post
)
from . import views

urlpatterns = [
    path('', views.home, name='sleduy-blog-home'),
    path('random/', random_post, name='sleduy-blog-random'),
    path('places/', PostListView.as_view(), name='sleduy-blog-places'),
    path('post/new/', postCreateView, name='post-create'),
    path('post/<int:pk>/', postDetailView, name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
	path('user/<str:username>', UserPostListView.as_view(), name='user-posts')
]