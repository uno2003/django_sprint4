from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import (DetailView, ListView, UpdateView,
                                  CreateView, DeleteView)
from django.contrib import messages
from django.views.generic.edit import FormMixin

from blog.models import Post, Category, User
from blog.forms import ChangePostForm, CommentForm
from blog.services import get_post, get_category, get_posts
from blog.services import get_post_comments
from blog.utils import PostMixin


class IndexView(ListView):
    model = Post
    ordering = 'id'
    paginate_by = 10
    template_name = 'blog/index.html'

    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self) -> QuerySet[Post]:
        return get_posts()


class PostDetailView(FormMixin, DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get(self, request, pk: int) -> HttpResponse:
        post = get_post(pk)
        context = {'post': post}
        context['form'] = CommentForm()
        context['comments'] = get_post_comments(post.id)
        return render(request, self.template_name, context)


class CategoryPostView(ListView):
    model = Category
    template_name = 'blog/category.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs) -> QuerySet[Category]:
        self.category, post_list = get_category(
            self.kwargs.get('category_slug')
        )
        return post_list

    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/create.html'
    form_class = ChangePostForm

    def get_success_url(self) -> HttpResponse:
        user = self.request.user.username
        return reverse_lazy('blog:profile', kwargs={'username': user})

    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form) -> HttpResponse:
        writer = User.objects.get(username=self.request.user)
        form.instance.author = writer
        if form.is_valid():
            self.object = form.save()
            form.instance = self.object
            form.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class PostUpdateView(PostMixin, UpdateView):

    def form_valid(self, form) -> HttpResponse:
        if form.is_valid():
            self.object = form.save()
            form.instance = self.object
            form.save()
            messages.add_message(
                self.request,
                messages.SUCCESS,
                'Новость исправлена'
            )
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class PostDeleteView(LoginRequiredMixin, PostMixin, DeleteView):
    def get_success_url(self) -> HttpResponse:
        return reverse('blog:index')
