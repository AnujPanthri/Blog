from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.shortcuts import reverse
class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')

    def get_by_slug(self, slug):
        return self.get_queryset().get(slug=slug)

class Post(models.Model):
    STATUS_CHOICES = (
    ('draft','Draft'),
    ('published','Published'),
    )
    
    title           =       models.CharField(max_length=100)
    slug            =       models.SlugField(unique=True, max_length=100)
    author          =       models.ForeignKey(User, related_name='blog_posts', on_delete=models.CASCADE)
    image           =       models.ImageField(upload_to='photos/%Y/%m/%d/',blank=True)
    content         =       models.TextField(blank=True)
    likes           =       models.ManyToManyField(User, related_name='likes', blank=True)
    created_date    =       models.DateTimeField(auto_now_add=True)
    update_date     =       models.DateTimeField(auto_now=True)
    status          =       models.CharField(max_length=20, choices=STATUS_CHOICES, default='published')

    objects = PostManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', args=[self.slug])


def create_slug(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.title)

pre_save.connect(create_slug, Post)

class Comment(models.Model):
    author = models.ForeignKey(User, related_name="user_comments", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    reply = models.ForeignKey('self', null=True, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}-{}".format(self.author.username, self.post.title)

    class Meta:
        ordering = ['-timestamp',]