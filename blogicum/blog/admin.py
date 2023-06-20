from django.contrib import admin
from .models import Post, Category, Location, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = [
        'title',
        'author',
        'category',
        'location',
        'text',
        'pub_date',
        'is_published',
        'image',
        'image_tag'
    ]
    list_display = (
        'title',
        'author',
        'category',
        'location',
        'pub_date',
        'is_published',
    )
    list_editable = ('is_published',)
    list_filter = ('category', 'location', 'author',)
    search_fields = ('title', 'author', 'category',)
    list_display_links = ('title',)
    readonly_fields = ['image_tag']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published',)
    list_editable = ('is_published',)
    search_fields = ('title',)
    list_display_links = ('title',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published',)
    list_editable = ('is_published',)
    search_fields = ('name',)
    list_display_links = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'post', 'author')
