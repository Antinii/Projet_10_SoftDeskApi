from rest_framework import serializers
from project.models import Project, Contributor, Issue, Comment


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'created_time']
   

class ProjectDetailSerializer(serializers.ModelSerializer):

    issues = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = "__all__"
    
    def get_issues(self, instance):
        queryset = instance.issues.filter(project=instance.id)
        serializer = IssueListSerializer(queryset, many=True)
        return serializer.data


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project']


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
    Serializer for issue details attached to a project
    """
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = "__all__"

    def get_comments(self, instance):
        queryset = Comment.objects.filter(issue_id=instance.id)
        serializer = CommentListSerializer(queryset, many=True)
        return serializer.data
