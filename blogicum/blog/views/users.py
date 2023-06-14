from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView

from blog.models import User

from blog.forms import ChangeUserProfileForm
from blog.models import Post


class UserLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('blog:index')


class UserLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'registration/logged_out.html'


class UserEditView(LoginRequiredMixin, UpdateView):
    template_name = 'blog/user.html'
    form_class = ChangeUserProfileForm
    success_url = reverse_lazy('blog:index')

    def get_object(self):
        return self.request.user


class UserProfileView(ListView):
    template_name = 'blog/profile.html'
    model = User
    paginate_by = 10
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_queryset(self, *args, **kwargs):
        self.user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=self.user).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.user
        return context





