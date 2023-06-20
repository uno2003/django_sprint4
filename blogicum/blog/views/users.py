import typing
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import QuerySet
from django.views.generic import ListView, UpdateView

from blog.forms import ChangeUserProfileForm
from blog.models import UserProfile
from blog.services import get_user_posts, get_user
from .mixins import RedirectToHomepageMixin


class UserLoginView(RedirectToHomepageMixin, LoginView):
    template_name = 'registration/login.html'


class UserLogoutView(LoginRequiredMixin, RedirectToHomepageMixin, LogoutView):
    template_name = 'registration/logged_out.html'


class UserEditView(LoginRequiredMixin, RedirectToHomepageMixin, UpdateView):
    template_name = 'blog/user.html'
    form_class = ChangeUserProfileForm

    def get_object(self) -> UserProfile:
        return self.request.user


class UserProfileView(ListView):
    template_name = 'blog/profile.html'
    model = UserProfile
    paginate_by = 10
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_object(self) -> UserProfile:
        return get_user(self.kwargs.get('username'))

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        return get_user_posts(self.get_object())

    def get_context_data(self, **kwargs) -> dict[str, typing.Any]:
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_object()
        return context
