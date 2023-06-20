from django.forms import ModelForm
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy

from blog.models import Post, Comment
from blog.forms import ChangePostForm, CommentForm


class RedirectToHomepageMixin:
    def get_success_url(self) -> HttpResponse:
        return reverse_lazy('blog:index')


class DispatchMixin:
    def dispatch(self,
                 request: HttpRequest,
                 *args,
                 **kwargs
                 ) -> HttpResponseRedirect:
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
    def form_valid(self, form: ModelForm) -> HttpResponse:
        form.instance.author = self.request.user
        if form.is_valid():
            form.instance = form.save()
            return super().form_valid(form)
        return self.form_invalid(form)


class PostMixin(DispatchMixin):
    model = Post
    template_name = 'blog/create.html'
    form_class = ChangePostForm
    url_key = 'pk'


class CommentMixin(DispatchMixin):
    model = Comment
    template_name = 'blog/comment.html'
    form_class = CommentForm
    url_key = 'post_id'
