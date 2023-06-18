from blog.views.posts import (IndexView, PostDetailView, CategoryPostView,
                              PostCreateView, PostUpdateView, PostDeleteView)
from blog.views.users import (UserLoginView, UserLogoutView,
                              UserEditView, UserProfileView)
from blog.views.comments import (CommentCreateView, CommentEditView,
                                 CommentDeleteView)

__all__ = (
    'posts',
    'users',
    'comments'
)
