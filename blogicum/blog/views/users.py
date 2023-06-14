from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, UpdateView, DeleteView


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


class UserProfileView(DetailView):
    template_name = 'blog/profile.html'
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_object()
        context['page_obj'] = self.get_queryset()
        return context

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        page_obj = Post.objects.filter(author=self.get_object())
        return page_obj


