from django.urls import path
from blog.views.posts import IndexView, PostDetailView, CategoryPostView
from blog.views.posts import PostCreateView, PostUpdateView, PostDeleteView
from blog.views.users import UserLoginView, UserLogoutView
from blog.views.users import UserEditView, UserProfileView
from blog.views.comments import add_comment, CommentEditView
from blog.views.comments import CommentDeleteView

app_name = 'blog'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path(
        'category/<slug:category_slug>/',
        CategoryPostView.as_view(),
        name='category_posts'
    ),
    path(
        'posts/<int:pk>/',
        PostDetailView.as_view(),
        name='post_detail'
    ),
    path(
        'posts/create/',
        PostCreateView.as_view(),
        name='create_post'
    ),
    path(
        'posts/<int:pk>/edit/',
        PostUpdateView.as_view(),
        name='edit_post'
    ),
    path(
        'posts/<int:pk>/delete/',
        PostDeleteView.as_view(),
        name='delete_post'
    ),
    path(
        'posts/<post_id>/edit_comment/<int:pk>',
        CommentEditView.as_view(),
        name='edit_comment'
    ),
    path(
        'posts/<post_id>/delete_comment/<int:pk>',
        CommentDeleteView.as_view(),
        name='delete_comment'
    ),
    path(
        '<int:pk>/comment/',
        add_comment,
        name='add_comment'
    ),
    path(
        'profile/<str:username>/',
        UserProfileView.as_view(),
        name='profile'),
    path(
        'user/',
        UserEditView.as_view(),
        name='edit_profile'
    ),
    path(
        'login/',
        UserLoginView.as_view(),
        name='login'
    ),
    path(
        'logout/',
        UserLogoutView.as_view(),
        name='logout'
    ),
]
