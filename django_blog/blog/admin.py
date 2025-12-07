from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ("title", "author", "published_date")
	search_fields = ("title", "content")
	list_filter = ("published_date",)

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ("post", "author", "created_at")
	search_fields = ("content",)
	list_filter = ("created_at",)
