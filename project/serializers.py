from rest_framework import serializers
from project.models import Project, Contributor
from issue.serializers import IssueListSerializer


class ProjectListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing projects.
    """
    class Meta:
        model = Project
        fields = ['id', 'created_time']


class ProjectDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for project details.
    """

    issues = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = "__all__"

    def get_issues(self, instance):
        queryset = instance.issues.filter(project=instance.id)
        serializer = IssueListSerializer(queryset, many=True)
        return serializer.data


class ContributorSerializer(serializers.ModelSerializer):
    """
    Serializer for contributors.
    """
    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project']
