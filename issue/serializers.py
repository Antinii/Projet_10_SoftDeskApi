from rest_framework import serializers
from issue.models import Issue
from project.models import Contributor
from comment.models import Comment
from comment.serializers import CommentListSerializer


class IssueListSerializer(serializers.ModelSerializer):
    """
    Serializer for Issue attached to a project
    """  
    class Meta:
        model = Issue
        fields = ['id']

    def create(self, validated_data):
        request = self.context.get('request')
        assigned_to_user = request.user
        contributor = Contributor.objects.get(user=assigned_to_user)
        validated_data['assigned_to'] = contributor
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')
        assigned_to_user = request.user
        assigned_to_contributor = Contributor.objects.get(user=assigned_to_user)
        instance.assigned_to = assigned_to_contributor
        instance.save()
        return instance


class IssueDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed issues attached to a project
    """
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = "__all__"

    def get_comments(self, instance):
        queryset = Comment.objects.filter(issue_id=instance.id)
        serializer = CommentListSerializer(queryset, many=True)
        return serializer.data
