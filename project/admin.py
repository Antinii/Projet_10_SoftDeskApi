from django.contrib import admin
from project.models import Project, Contributor, Issue, Comment


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'author', 'created_time')


class ContributorAdmin(admin.ModelAdmin):
    list_display = ('user', 'project')


class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'balise', 'status', 'project')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('description', 'author', 'issue')



admin.site.register(Project, ProjectAdmin)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Comment, CommentAdmin)
