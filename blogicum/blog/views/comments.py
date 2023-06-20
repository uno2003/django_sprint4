from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView

from blog.forms import CommentForm
from blog.models import Comment
from .mixins import CommentMixin


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'blog/comment.html'
    form_class = CommentForm

    def form_valid(self, form: CommentForm) -> CommentForm:
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse(
            'blog:post_detail',
            kwargs=dict(pk=self.kwargs['pk'])
        )


class CommentEditView(LoginRequiredMixin, CommentMixin, UpdateView):

    def form_valid(self, form: CommentForm) -> CommentForm:
        form.instance.author = self.request.user
        return super().form_valid(form)


class CommentDeleteView(LoginRequiredMixin, CommentMixin, DeleteView):
    pass
