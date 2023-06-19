from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Count

from blog.models import Category, Post, Comment, User


def get_post_comments(post_id) -> QuerySet[Comment]:
    return Comment.objects.select_related('post').filter(post__id=post_id)


def get_user_posts(user) -> QuerySet[Post]:
    return (
        Post.objects.
        annotate(comment_count=Count('comments'))
        .filter(author=user)
        .order_by('-pub_date')
    )


def get_posts() -> QuerySet[Post]:
    post_list = (
        Post.objects
        .select_related('category')
        .annotate(comment_count=Count('comments'))
        .filter(is_published=True,
                category__is_published=True,
                pub_date__lte=timezone.now()).order_by('-pub_date')

    )

    return post_list


def get_post(id: int) -> Post:
    return get_object_or_404(get_posts(), id=id)


def get_category(category_slug: str) -> tuple[Category, QuerySet[Post]]:
    category = get_object_or_404(
        Category.objects
        .only('title', 'description')
        .filter(slug=category_slug,
                is_published=True)
    )
    post_list = get_posts().filter(category=category)
    return category, post_list


def get_user(kwargs) -> str:
    user = get_object_or_404(User, username=kwargs.get('username'))
    return user
