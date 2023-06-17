from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView

from blog.forms import ChangeUserProfileForm
from blog.models import User
from blog.services import get_user_posts, get_user


class UserRedirectMixin:
    success_url = reverse_lazy('blog:index')


class UserLoginView(UserRedirectMixin, LoginView):
    template_name = 'registration/login.html'


class UserLogoutView(LoginRequiredMixin, UserRedirectMixin, LogoutView):
    template_name = 'registration/logged_out.html'


class UserEditView(LoginRequiredMixin, UserRedirectMixin, UpdateView):
    template_name = 'blog/user.html'
    form_class = ChangeUserProfileForm

    def get_object(self) -> User:
        return self.request.user


class UserProfileView(ListView):
    template_name = 'blog/profile.html'
    model = User
    paginate_by = 10
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        self.user = get_user(self.kwargs)
        return get_user_posts(self.user)

    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context['profile'] = self.user
        return context
