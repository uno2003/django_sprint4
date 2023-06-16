from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView

from blog.forms import CommentForm
from blog.models import Comment


class CommentMixin:
    model = Comment
    template_name = 'blog/comment.html'
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != self.request.user:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs=dict(pk=self.kwargs['post_id'])
        )


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'blog/comment.html'
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs=dict(pk=self.kwargs['pk'])
        )


class CommentEditView(LoginRequiredMixin, CommentMixin, UpdateView):

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CommentDeleteView(LoginRequiredMixin, CommentMixin, DeleteView):
    pass
