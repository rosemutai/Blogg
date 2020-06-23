from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse

User = get_user_model()

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=20)
    
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    comments = models.IntegerField(default=True)
    post_image = models.ImageField(default='')
    featured = models.BooleanField()
    body = models.TextField()
    user = models.ManyToManyField(User, blank=True)
    

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'pk': str(self.id)})
    
    def __str__(self):
        return self.title

class PostComment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)