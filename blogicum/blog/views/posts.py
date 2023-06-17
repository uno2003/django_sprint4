from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import (HttpResponse,
                         HttpResponsePermanentRedirect,
                         HttpResponseRedirect)
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, UpdateView
from django.views.generic import CreateView, DeleteView
from django.contrib import messages
from django.views.generic.edit import FormMixin

from blog.models import Post, Category, User
from blog.forms import ChangePostForm, CommentForm
from blog.services import get_post, get_category, get_posts
from blog.services import get_post_comments


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


class PostMixin:
    model = Post
    template_name = 'blog/create.html'
    form_class = ChangePostForm

    def dispatch(self, request, *args, **kwargs) -> (
            HttpResponsePermanentRedirect | HttpResponseRedirect):
        post = self.get_object()
        if (not request.user.is_authenticated
                or post.author != self.request.user):
            return redirect('blog:post_detail', pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse('blog:post_detail', kwargs=dict(pk=self.kwargs['pk']))


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
    model = Post
    form_class = ChangePostForm
    template_name = 'blog/create.html'

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
    def get_success_url(self):
        return reverse('blog:index')
