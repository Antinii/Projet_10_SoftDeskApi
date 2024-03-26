from django.contrib import admin
from project.models import Project, Contributor


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'author', 'created_time')


class ContributorAdmin(admin.ModelAdmin):
    list_display = ('user', 'project')


admin.site.register(Project, ProjectAdmin)
admin.site.register(Contributor, ContributorAdmin)
