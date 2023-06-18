from .posts import (IndexView, PostDetailView, CategoryPostView,
                    PostCreateView, PostUpdateView, PostDeleteView)
from .users import (UserLoginView, UserLogoutView,
                    UserEditView, UserProfileView)
from .comments import (CommentCreateView, CommentEditView,
                       CommentDeleteView)
__all__ = (
    'comments',
    'posts',
    'users'
)
