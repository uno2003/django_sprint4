from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth import logout

from blog.models import User


class UserLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('blog:index')


class UserLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'registration/logged_out.html'


class UserEditView(LoginRequiredMixin, UpdateView):
    template_name = 'blog/user.html'
    success_url = reverse_lazy('blog:index')

    def get_object(self) -> object:
        return self.request.user

class UserProfileView(LoginRequiredMixin, DetailView):
    template_name = 'blog/profile.html'
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UserDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'main/delete_user.html'
    success_url = reverse_lazy('blog:index')

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS,
                             'Пользователь удален')

        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

class PasswordsChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'registration/password_change_form.html'
    success_url = 'blog:index'