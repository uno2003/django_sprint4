from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, Post


class ChangeUserProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты.')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',)


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email',)


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'author',
            'location',
            'category',
            'image'
        ]
        widget = {'author': forms.HiddenInput}