from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import PostComment

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

class CommentForm(forms.ModelForm):
   
    class Meta:
        model = PostComment
        fields =  ('content',)

  


    