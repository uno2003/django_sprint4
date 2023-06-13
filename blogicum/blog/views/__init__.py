from blog.views.posts import IndexView, PostDetailView, CategoryPostView, AddPostView, EditPostView, DeletePostView, CommentCreateView
from blog.views.users import UserLogoutView, UserEditView, UserLoginView, UserProfileView, UserDeleteView, PasswordsChangeView
from blog.views.errors import page_not_found, internal_server_error, csrf_failure

# __all__ = (
#     'IndexView',
#     'PostDetailView',
#     'CategoryPostView',
#     'AddPostView',
#     'EditPostView',
#     'DeleteUserView',
#     'UserLogoutView',
#     'UserEditView',
#     'UserLoginView',
#     'ProfileView',
#     'PasswordsChangeView',
#     'page_not_found',
#     'internal_server_error',
#     'csrf_failure',
# )