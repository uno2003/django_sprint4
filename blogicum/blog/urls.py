from django.urls import path
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .views.posts import *
from .views.users import *

app_name = 'blog'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('category/<slug:category_slug>/',
         CategoryPostView.as_view(), name='category_posts'),
    path('create/', PostCreateView.as_view(), name='create_post'),
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='edit_post'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='delete_post'),

    path('<int:pk>/comment/', add_comment, name='add_comment'),
    path('posts/<post_id>/edit_comment/<int:pk>', CommentEditView.as_view(), name='edit_comment'),
    path('posts/<post_id>/delete_comment/<int:pk>', CommentDeleteView.as_view(), name='delete_comment'),

    path('profile/<username>/', UserProfileView.as_view(), name='profile'),
    path('user/', UserEditView.as_view(), name='edit_profile'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
