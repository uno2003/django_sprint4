from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from blog.models import Post, Comment
from blog.forms import ChangePostForm, CommentForm


class DispatchMixin:
    def dispatch(self, request, *args, **kwargs) -> HttpResponseRedirect:
        obj = self.get_object()
        if (not request.user.is_authenticated
                or obj.author != self.request.user):
            return redirect('blog:post_detail', pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse(
            'blog:post_detail',
            kwargs=dict(pk=self.kwargs[self.url_key])
        )


class PostFormValidationMixin:
    def form_valid(self, form) -> HttpResponse:
        form.instance.author = self.request.user
        if form.is_valid():
            self.object = form.save()
            form.instance = self.object
            form.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class PostMixin(DispatchMixin):
    model = Post
    template_name = 'blog/create.html'
    form_class = ChangePostForm
    url_key = 'pk'

    def form_valid(self, form) -> HttpResponse:
        form.instance.author = self.request.user
        if form.is_valid():
            self.object = form.save()
            form.instance = self.object
            form.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class CommentMixin(DispatchMixin):
    model = Comment
    template_name = 'blog/comment.html'
    form_class = CommentForm
    url_key = 'post_id'
