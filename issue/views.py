from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from issue.models import Issue
from project.permissions import IsAuthorPermission, IssuePermission
from issue.serializers import IssueDetailSerializer, IssueListSerializer
from project.models import Contributor
from project.views import MultipleSerializerMixin


class IssueViewSet(MultipleSerializerMixin, viewsets.ModelViewSet):

    queryset = Issue.objects.all()
    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    permission_classes = [IsAuthenticated, IsAuthorPermission, IssuePermission]

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return self.detail_serializer_class
        return super().get_serializer_class()

    def perform_create(self, serializer):
        author = self.request.user
        project_id = self.request.data.get("project")
        if not Contributor.objects.filter(user=author, project=project_id).exists():
            raise PermissionDenied("Seuls les contributeurs du projet peuvent créer un problème.")

        assignee_id = self.request.data.get("assigned_to")
        if assignee_id:
            if not Contributor.objects.filter(user_id=assignee_id, project_id=project_id).exists():
                raise PermissionDenied("L'utilisateur assigné doit être un contributeur du projet.")
        serializer.save(author=author, project_id=project_id)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
