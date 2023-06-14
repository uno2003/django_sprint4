from django.urls import path

from .views import IndexView, PostDetailView, CategoryPostView, AddPostView, UserProfileView, UserLogoutView, UserLoginView, EditPostView, DeletePostView, CommentCreateView

app_name = 'blog'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('category/<slug:category_slug>/',
         CategoryPostView.as_view(), name='category_posts'),
    path('create/', AddPostView.as_view(), name='create_post'),
    path('post/<int:pk>/edit', EditPostView.as_view(), name='edit_post'),
    path('post/<int:pk>/delete', DeletePostView.as_view(), name='delete_post'),


    path('<int:pk>/comment/', CommentCreateView.as_view(), name='add_comment'),

    path('profile/<str:username>/', UserProfileView.as_view(), name='profile'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    # path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    # path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    # path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
