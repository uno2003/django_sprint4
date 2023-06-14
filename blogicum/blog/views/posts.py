from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView
from django.contrib import messages

from blog.models import Post, Category, User, Comment
from blog.forms import AddPostForm, CommentForm
from blog.services import get_post, get_category, get_posts, get_user_page
from django.views.generic.edit import FormMixin


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', pk=pk)

class IndexView(ListView):
    model = Post
    ordering = 'id'
    paginate_by = 10
    template_name = 'blog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['comment_count'] = Comment.objects.get(post=post)
        return context

    def get_queryset(self):
        return get_posts()



class PostDetailView(FormMixin, DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get(self, request, pk: int) -> HttpResponse:
        post = get_post(pk)
        context = {'post': post}
        context['form'] = CommentForm()
        context['comments'] = Comment.objects.select_related('post').filter(post__id=post.id)
        return render(request, self.template_name, context)



class CategoryPostView(DetailView):
    model = Category
    template_name = 'blog/category.html'

    def get_queryset(self, *args, **kwargs):
        self.category = get_object_or_404(User, username=self.kwargs.get('category_slug'))
        return Post.objects.filter(category=self.category).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.user
        return context

    def get(self, request, category_slug: str) -> HttpResponse:
        category, post_list = get_category(category_slug)
        context = {'category': category,
                   'post_list': post_list}
        return render(request, self.template_name, context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/create.html'
    form_class = AddPostForm

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
    form_class = AddPostForm
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


class CommentCreateView(CreateView):
    post = None
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        self.post = get_object_or_404(Post, pk=kwargs['pk'], author=request.user)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post:detail', kwargs={'pk': self.post.pk})

class CommentEditView(LoginRequiredMixin, UpdateView):
    model = Comment
    template_name = 'blog/comment.html'
    success_url = reverse_lazy('blog:index')



class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment.html'
    success_url = reverse_lazy('blog:index')
