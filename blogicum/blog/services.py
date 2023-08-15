from django.db.models import QuerySet, Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Count

from blog.models import Category, Post, Comment, UserProfile


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
    posts = (
        Post.objects
        .select_related('category')
        .annotate(comment_count=Count('comments'))
        .filter(is_published=True,
                category__is_published=True,
                pub_date__lte=timezone.now())
        .order_by('-pub_date')
    )
    return posts


def get_posts_list(user=None) -> QuerySet[Post]:
    posts = (
        Post.objects
        .select_related('category')
        .annotate(comment_count=Count('comments'))
        .filter(Q(is_published=True) | Q(author=user),
                category__is_published=True,
                pub_date__lte=timezone.now())
        .order_by('-pub_date')
    )
    return posts


def get_post(id: int) -> Post:
    return get_object_or_404(get_posts(), id=id)


def get_category(category_slug: str) -> tuple[Category, QuerySet[Post]]:
    category = get_object_or_404(
        Category.objects
        .only('title', 'description')
        .filter(slug=category_slug,
                is_published=True)
    )
    posts = get_posts().filter(category=category)
    return category, posts


def get_user(username) -> UserProfile:
    user = get_object_or_404(UserProfile, username=username)
    return user
