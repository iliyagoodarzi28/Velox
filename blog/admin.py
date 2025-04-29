from django.contrib import admin
from .models import Category, Blog, Comment, Rating

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)

admin.site.register(Category)


class BlogAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'get_persian_date', 'views')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)
    search_fields = ('name', 'description')
    list_filter = ('category', 'date')

admin.site.register(Blog)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('blog', 'name', 'email', 'get_persian_created_at')
    ordering = ('-created_at',)
    search_fields = ('name', 'email', 'content')
    list_filter = ('created_at',)

admin.site.register(Comment)


class RatingAdmin(admin.ModelAdmin):
    list_display = ('blog', 'user', 'score')
    ordering = ('blog', 'user')
    search_fields = ('blog__name', 'user__username')
    list_filter = ('score',)

admin.site.register(Rating)
