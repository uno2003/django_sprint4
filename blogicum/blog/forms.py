from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _
from .models import UserProfile, Post, Comment


class ChangeUserProfileForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            "Для смены пароля перейдите по "
            '<a href="../auth/password_change/">ссылке</a>.'
        ),
    )

    class Meta:
        model = UserProfile
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'avatar',
        )


class RegisterUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserProfile
        fields = (
            'username',
            'first_name',
            'last_name',
            'email'
        )


class ChangePostForm(forms.ModelForm):
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
