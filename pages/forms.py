from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from users.models import ProfilePage
from .models import Comments


class CreateForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username', 'email','password1','password2']

class LoginForm(forms.Form):
    username=forms.CharField(max_length=50)
    password=forms.CharField(max_length=50,widget=forms.PasswordInput)
    

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = ProfilePage
        fields = ['image']        

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comments
        fields=['name','body']
       