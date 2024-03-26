from django.db import models
from django.conf import settings
import uuid
from issue.models import Issue


class Comment(models.Model):
    """
    Model representing a comment attached to an issue
    """

    created_time = models.DateTimeField(auto_now_add=True)

    description = models.TextField(max_length=2048)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comment_author')
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE, related_name='comments')
