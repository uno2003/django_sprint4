from django.urls import path

from .views import IndexView, PostDetailView, CategoryPostView, AddPostView, ProfileView, LogoutView, LoginView

app_name = 'blog'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('posts/<int:id>/', PostDetailView.as_view(), name='post_detail'),
    path('category/<slug:category_slug>/',
         CategoryPostView.as_view(), name='category_posts'),
    path('create/', AddPostView.as_view(), name='create_post'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
