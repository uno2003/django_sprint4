from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, UpdateView
from django.views.generic import CreateView, DeleteView
from django.contrib import messages
from django.views.generic.edit import FormMixin

from blog.models import Post, Category, User
from blog.forms import ChangePostForm, CommentForm
from blog.services import get_post, get_category, get_posts
from blog.services import get_post_comments, get_comments_count


class IndexView(ListView):
    model = Post
    ordering = 'id'
    paginate_by = 10
    template_name = 'blog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        post_list = get_posts()
        return get_comments_count(post_list)


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

    def get_queryset(self, *args, **kwargs):
        self.category, post_list = get_category(
            self.kwargs.get('category_slug')
        )
        return get_comments_count(post_list)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/create.html'
    form_class = ChangePostForm

    def get_success_url(self):
        user = self.request.user.username
        return reverse_lazy('blog:profile', kwargs={'username': user})

    def get_context_data(self, **kwargs) -> dict:
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


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = ChangePostForm
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')

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


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')
