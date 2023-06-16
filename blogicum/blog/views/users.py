from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView

from blog.forms import ChangeUserProfileForm
from blog.models import User
from blog.services import get_user_posts, get_user, get_comments_count


class UserRedirectMixin:
    success_url = reverse_lazy('blog:index')


class UserLoginView(UserRedirectMixin, LoginView):
    template_name = 'registration/login.html'


class UserLogoutView(LoginRequiredMixin, UserRedirectMixin, LogoutView):
    template_name = 'registration/logged_out.html'


class UserEditView(LoginRequiredMixin, UserRedirectMixin, UpdateView):
    template_name = 'blog/user.html'
    form_class = ChangeUserProfileForm

    def get_object(self):
        return self.request.user


class UserProfileView(ListView):
    template_name = 'blog/profile.html'
    model = User
    paginate_by = 10
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_queryset(self, *args, **kwargs):
        self.user = get_user(self.kwargs)
        return get_comments_count(get_user_posts(self.user))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.user
        return context
