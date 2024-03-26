from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from project.models import Project, Contributor
from project.permissions import IsAuthorPermission, ProjectPermission, ContributorPermission, PermissionDenied
from project.serializers import ProjectListSerializer, ProjectDetailSerializer, ContributorSerializer


class MultipleSerializerMixin:

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()
    

class ProjectViewSet(MultipleSerializerMixin, viewsets.ModelViewSet):

    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    permission_classes = [IsAuthenticated, IsAuthorPermission, ProjectPermission]

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return self.detail_serializer_class
        return super().get_serializer_class()
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user, contributors=[user])

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, ContributorPermission]

    def perform_create(self, serializer):
        project = self.request.data.get("project")
        if Project.objects.get(id=project).author == self.request.user:
            serializer.save()
        else:
            raise PermissionDenied(
                "Vous devez être l'auteur du projet pour ajouter des contributeurs."
            )
