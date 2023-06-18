from blog.views.posts import (IndexView, PostDetailView, CategoryPostView,
                              PostCreateView, PostUpdateView, PostDeleteView)
from blog.views.users import (UserLoginView, UserLogoutView,
                              UserEditView, UserProfileView)
from blog.views.comments import (CommentCreateView, CommentEditView,
                                 CommentDeleteView)

__all__ = [
    'IndexView',
    'PostDetailView',
    'CategoryPostView',
    'PostCreateView',
    'PostUpdateView',
    'PostDeleteView',
    'UserLoginView',
    'UserLogoutView',
    'UserEditView',
    'UserProfileView',
    'CommentCreateView',
    'CommentEditView',
    'CommentDeleteView'
]
