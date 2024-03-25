from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


class Project(models.Model):
    """
    Model representing a project, with his types, the created time, the title, the description,
    the author and the contributors.
    """

    PROJECT_TYPE = [('BACK-END', 'back-end'),
                    ('FRONT-END', 'front-end'),
                    ('IOS', 'iOS'),
                    ('ANDROID', 'android')
    ]

    created_time = models.DateTimeField(auto_now_add=True)

    title = models.CharField(max_length=255)
    description = models.TextField(max_length=2048)
    type = models.CharField(max_length=64, choices=PROJECT_TYPE)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='project_author')

    contributors = models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='Contributor', related_name='project_contributors')



class Contributor(models.Model):
    """
    Model representing a contributor to a project, a contributor is linked to an user and to a project.
    """

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.user
    
    @receiver(post_save, sender=Project)
    def create_author_contributor(sender, instance, created, **kwargs):
        if created:
            Contributor.objects.create(user=instance.author, project=instance)
    

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
    assigned_to = models.ForeignKey(to=Contributor, on_delete=models.SET_NULL, blank=True, null=True, related_name='assigned_issues')


class Comment(models.Model):
    """
    Model representing a comment attached to an issue
    """

    created_time = models.DateTimeField(auto_now_add=True)

    description = models.TextField(max_length=2048)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comment_author')
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE, related_name='comments')
