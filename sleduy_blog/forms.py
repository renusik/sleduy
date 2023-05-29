from django import forms
from django.forms import ClearableFileInput
from .models import Images, Post


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=100, label='Название')
    content = forms.CharField(max_length=10000, label='Описание')
    short_content = forms.CharField(max_length=150, label='Краткое описание')
    work_hours = forms.CharField(max_length=100, label='Время работы')
    
    class Meta:
        model = Post
        fields = ('title', 'content', 'short_content', 'work_hours')


class ImageForm(PostForm):
    image = forms.ImageField(
        label='Фото', 
        widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True})
    )    
    
    class Meta(PostForm.Meta):
        fields = PostForm.Meta.fields + ('image', )