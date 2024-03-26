from django.contrib import admin
from comment.models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('description', 'author', 'issue')


admin.site.register(Comment, CommentAdmin)
