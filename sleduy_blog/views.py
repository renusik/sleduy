from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User

from .forms import ImageForm, PostForm
from .models import Post, Images
import random

from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect

def places(request):
	return render(
        request, 'sleduy_blog/places.html', {
    	    'posts': Post.objects.all()
	    }
    )

def home(request):
	return render(
        request, 'sleduy_blog/home.html'
    )

def random_post(request):
    post_count = Post.objects.all().count()  
    random_val = random.randint(0, post_count-1)  
    post_id = Post.objects.values_list('id', flat=True)[random_val]   
    return redirect('post-detail', pk=post_id)


def postDetailView(request, pk):
    post = get_object_or_404(Post, pk=pk)
    photos = Images.objects.filter(post=post)
    return render(request, 'sleduy_blog/post_detail.html', {
        'post': post,
        'photos': photos
    })


class PostListView(ListView):
    model = Post
    template_name = 'sleduy_blog/places.html'  
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


@login_required
def postCreateView(request):
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST)
        images = request.FILES.getlist('image')
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            short_content = form.cleaned_data['short_content']
            work_hours = form.cleaned_data['work_hours']
            author = request.user

            post = Post.objects.create(
                author=author, 
                title=title, 
                content=content, 
                short_content=short_content, 
                work_hours=work_hours
            )

            for i in images:
                Images(post=post, image=i).save()

    return render(request, 'sleduy_blog/post_form.html')


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'sleduy_blog/post_update.html'
    fields = ['title', 'content', 'work_hours', 'short_content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'sleduy_blog/post_delete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False




class UserPostListView(ListView):
    model = Post
    template_name = 'sleduy_blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
