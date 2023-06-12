from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, LoginView, LogoutView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, UpdateView, DeleteView, CreateView
from django.contrib import messages
from django.contrib.auth import logout

from .models import Post, Category, User
from .services import get_post, get_limit_posts, get_category
from .forms import RegisterUserForm, AddPostForm

DEFAULT_LIMIT_POSTS = 5

def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, reason=''):
    return render(request, 'pages/403csrf.html', status=403)

def internal_server_error(request):
    return render(request, 'pages/500.html', status=500)



class UserLoginView(LoginView):
    template_name = 'registration/login.html'


class DjangoLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'registration/logged_out.html'


class UserEditView(LoginRequiredMixin, UpdateView):
    template_name = 'blog/user.html'
    success_url = reverse_lazy('blog:index')

    def get_object(self) -> object:
        return self.request.user

class ProfileView(LoginRequiredMixin, DetailView):
    template_name = 'blog/profile.html'
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    context_object_name = 'User'


    def get_object(self):
        object = get_object_or_404(User, username=self.kwargs.get("username"))



class DeleteUserView(LoginRequiredMixin, DeleteView):
    template_name = 'main/delete_user.html'
    success_url = reverse_lazy('blog:index')

    def setup(self, request, *args, **kwargs):
        self.user_id = get_user_pk(request)
        return super().setup(request, *args, **kwargs)

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

class IndexView(ListView):
    model = Post
    paginate_by = 10
    template_name = 'blog/index.html'
    context_object_name = 'posts_list'

    def get_context_data(self) -> dict:
        page_obj = get_limit_posts(limit=DEFAULT_LIMIT_POSTS)
        context = {'page_obj': page_obj}
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get(self, request, id: int) -> HttpResponse:
        post = get_post(id)
        context = {'post': post}
        return render(request, self.template_name, context)


class CategoryPostView(DetailView):
    model = Category
    template_name = 'blog/category.html'

    def get(self, request, category_slug: str) -> HttpResponse:
        category, post_list = get_category(category_slug)
        context = {'category': category,
                   'post_list': post_list}
        return render(request, self.template_name, context)


class AddPostView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/create.html'
    form_class = AddPostForm
    success_url = reverse_lazy('blog:index')

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form) -> HttpResponse:
        writer = User.objects.get(username=self.request.user)
        form.instance.author = writer
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
