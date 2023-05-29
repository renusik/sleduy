from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


def get_image_filename(instance, filename):
    title = instance.post.title
    slug = slugify(title)
    return "images/%s-%s" % (slug, filename) 

class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    content = models.TextField(verbose_name='Описание')
    short_content = models.CharField(max_length=150, verbose_name='Краткое описание', default='', 
        help_text='Максимум 150 символов'
    )
    work_hours = models.CharField(max_length=100, verbose_name='Время работы', default='')
    date_posted = models.DateTimeField(default=timezone.now, verbose_name='Дата')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Images(models.Model):
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)
    image = models.FileField(upload_to=get_image_filename, verbose_name='Image')
 
    def __str__(self):
        return self.post.title
