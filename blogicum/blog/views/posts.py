import typing
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (DetailView, ListView, UpdateView,
                                  CreateView, DeleteView)
from django.views.generic.edit import FormMixin

from blog.models import Post, Category
from blog.forms import ChangePostForm, CommentForm
from blog.services import get_post, get_category, get_posts, get_post_comments
from .mixins import (PostMixin, PostFormValidationMixin,
                     RedirectToHomepageMixin)


class IndexView(ListView):
    model = Post
    ordering = 'id'
    paginate_by = 10
    template_name = 'blog/index.html'

    def get_queryset(self) -> QuerySet[Post]:
        return get_posts()


class PostDetailView(FormMixin, DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
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
        self.category, posts = get_category(
            self.kwargs.get('category_slug')
        )
        return posts

    def get_context_data(self, **kwargs) -> dict[str, typing.Any]:
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class PostCreateView(LoginRequiredMixin, PostFormValidationMixin, CreateView):
    model = Post
    template_name = 'blog/create.html'
    form_class = ChangePostForm

    def get_success_url(self) -> HttpResponse:
        user = self.request.user.username
        return reverse_lazy('blog:profile', kwargs={'username': user})


class PostUpdateView(PostMixin, PostFormValidationMixin, UpdateView):
    pass


class PostDeleteView(LoginRequiredMixin, RedirectToHomepageMixin,
                     PostMixin, DeleteView):
    pass
