from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _
from .models import User, Post, Comment


class ChangeUserProfileForm(UserChangeForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты.')
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            "Для смены пароля перейдите по "
            '<a href="../auth/password_change/">ссылке</a>.'
        ),
    )
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
            'location',
            'category',
            'pub_date',
            'is_published',
            'image'
        ]
        widget = {'author': forms.HiddenInput}

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)