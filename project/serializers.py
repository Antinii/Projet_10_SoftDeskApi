from rest_framework import serializers
from project.models import Project, Contributor, Issue, Comment


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author', 'created_time']
   

class ProjectDetailSerializer(serializers.ModelSerializer):

    issues = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'created_time', 'title', 'description', 'type', 'author', 'contributors', 'issues']
    
    def get_issues(self, instance):
        queryset = instance.issues.filter(project=instance.id)
        serializer = IssueListSerializer(queryset, many=True)
        return serializer.data


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project']


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for comments attached to an issue
    """
    class Meta:
        model = Comment
        fields = ['id', 'description', 'author', 'issue', 'created_time']


class IssueListSerializer(serializers.ModelSerializer):
    """
    Serializer for Issue attached to a project
    """
    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'priority', 'balise', 'status', 'project']


class IssueDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for issue details attached to a project
    """
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'priority', 'balise', 'status', 'project', 'author', 'created_time', 'comments', 'assigned_to']

    def get_comments(self, instance):
        queryset = Comment.objects.filter(issue_id=instance.id)
        serializer = CommentSerializer(queryset, many=True)
        return serializer.data
