from django.contrib import admin
from issue.models import Issue


class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'balise', 'status', 'project')


admin.site.register(Issue, IssueAdmin)
