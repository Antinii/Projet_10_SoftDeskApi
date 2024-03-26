from rest_framework import serializers
from comment.models import Comment


class CommentListSerializer(serializers.ModelSerializer):
    """
    Serializer for comments attached to an issue
    """
    class Meta:
        model = Comment
        fields = ['id']


class CommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
