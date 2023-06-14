from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView
from django.contrib import messages

from blog.models import Post, Category, User, Comment
from blog.forms import AddPostForm, CommentForm
from blog.services import get_post, get_category
from django.views.generic.edit import FormMixin


class IndexView(ListView):
    model = Post
    ordering = 'id'
    paginate_by = 10
    template_name = 'blog/index.html'


# class PostDetailView(DetailView):
#     model = Post
#     template_name = 'blog/detail.html'
#     pk_url_kwarg = 'id'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # context['form'] = CommentForm()
#         # context['comment'] = (
#         #     self.object.comment.select_related('author')
#         # )
#         return context


class PostDetailView(FormMixin, DetailView):
    model = Post
    template_name = 'blog/detail.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm
        context['comments'] = (
            self.object.comment.select_related('author')
        )
        return context



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
        if form.is_valid():
            self.object = form.save()
            form.instance = self.object
            form.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class EditPostView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/create.html'
    form_class = AddPostForm

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        return context

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


class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')



class CommentCreateView(FormMixin, DetailView):
    model = Post
    template_name = 'blog/comment.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

# class CommentCreateView(CreateView):
#     post_obj = None
#     model = Comment
#     form_class = CommentForm


    # def dispatch(self, request, *args, **kwargs):
    #     self.post_obj = get_object_or_404(Post, pk=kwargs['pk'])
    #     return super().dispatch(request, *args, **kwargs)

    #
    # def post(self, request, pk):
    #     post = Post.objects.get(id=pk)
    #     form = CommentForm(request.POST)
    #     if form.is_valid():
    #         comment = form.save(commit=False)
    #         comment.post = post
    #         comment.author = request.user
    #         comment.save()
    #     return redirect('blog:post_detail', pk=pk)
    #
    # def get(self, request, post_id):
    #     form = CommentForm()
    #     return render(request, 'comment.html', {'form': form})

    # def form_valid(self, form):
    #     form.instance.author = self.request.user
    #     form.instance.post = self.post_obj
    #     return super().form_valid(form)
    #
    # def get_success_url(self):
    #     return reverse('blog:post_detail', kwargs={'pk': self.post_obj.pk})

