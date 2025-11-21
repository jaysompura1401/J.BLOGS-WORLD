from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment
from django.core.validators import RegexValidator

class RegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=50,
        help_text='Use any characters (1-50).',
        validators=[RegexValidator(regex=r'^.{1,50}$', message='Username must be 1-50 characters.')]
    )
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username','email','password1','password2')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','content','cover','categories','tags','status')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
