from blog.models import Post, Comment

from blog.forms import ChangePostForm, CommentForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse


class DispatchMixin:
    def dispatch(self, request, *args, **kwargs) -> HttpResponseRedirect:
        obj = self.get_object()
        if (not request.user.is_authenticated
                or obj.author != self.request.user):
            return redirect('blog:post_detail', pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)


class PostMixin(DispatchMixin):
    model = Post
    template_name = 'blog/create.html'
    form_class = ChangePostForm

    def get_success_url(self) -> str:
        return reverse('blog:post_detail', kwargs=dict(pk=self.kwargs['pk']))


class CommentMixin(DispatchMixin):
    model = Comment
    template_name = 'blog/comment.html'
    form_class = CommentForm

    def get_success_url(self) -> str:
        return reverse(
            'blog:post_detail',
            kwargs=dict(pk=self.kwargs['post_id'])
        )
