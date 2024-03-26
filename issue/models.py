from django.db import models
from django.conf import settings
from project.models import Project, Contributor


class Issue(models.Model):
    """
    Model representing an issue, specifying the problems of a project.
    """

    PRIORITY = [('LOW', 'Low'),
                ('MEDIUM', 'Medium'),
                ('HIGH', 'High')]

    BALISE = [('BUG', 'Bug'),
              ('FEATURE', 'Feature'),
              ('TASK', 'Task')]

    STATUS = [('TODO', 'To Do'),
              ('IN PROGRESS', 'In Progress'),
              ('FINISHED', 'Finished')]

    created_time = models.DateTimeField(auto_now_add=True)

    title = models.CharField(max_length=255)
    description = models.TextField(max_length=2048)
    priority = models.CharField(max_length=64, choices=PRIORITY)
    balise = models.CharField(max_length=64, choices=BALISE)
    status = models.CharField(max_length=64, choices=STATUS, default='TODO')
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name='issues')
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='issue_author')
    assigned_to = models.ForeignKey(to=Contributor, on_delete=models.SET_NULL,
                                    blank=True, null=True, related_name='assigned_issues')
