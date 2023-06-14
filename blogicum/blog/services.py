from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.utils import timezone

from blog.models import Category, Post


def get_posts() -> QuerySet[Post]:
    post_list = (
        Post.objects
        .select_related('category')
        .filter(is_published=True,
                category__is_published=True,
                pub_date__lte=timezone.now())
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
