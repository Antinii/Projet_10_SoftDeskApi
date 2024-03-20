from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from project.models import Project, Contributor, Issue, Comment
from project.permissions import IsAuthorPermission, ProjectPermission, ContributorPermission, IssuePermission, CommentPermission
from project.serializers import ProjectListSerializer, ProjectDetailSerializer, ContributorSerializer, IssueDetailSerializer, IssueListSerializer, CommentSerializer


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

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user, contributors=[user])
   

class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsAuthorPermission, ContributorPermission]

    def perform_create(self, serializer):
        project = self.request.data.get("project")
        if Project.objects.get(id=project).author == self.request.user:
            serializer.save()
        else:
            raise PermissionDenied(
                "Vous devez être l'auteur du projet pour ajouter des contributeurs."
            )


class IssueViewSet(MultipleSerializerMixin, viewsets.ModelViewSet):

    queryset = Issue.objects.all()
    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    permission_classes = [IsAuthenticated, IsAuthorPermission, IssuePermission]

    def perform_create(self, serializer):
        author = self.request.user
        project_id = self.request.data.get("project")
        if not Contributor.objects.filter(user__pk=author.id, project__pk=project_id).exists():
            raise PermissionDenied("Seuls les contributeurs du projet peuvent créer un problème.")

        assignee_id = self.request.data.get("assigned_to", None)
        if assignee_id:
            is_contributor = Contributor.objects.filter(
                user__pk=assignee_id, project__pk=project_id
            ).exists()
            if not is_contributor:
                raise PermissionDenied("L'utilisateur assigné doit être un contributeur du projet.")
        serializer.save(author=author)
    

class CommentViewSet(MultipleSerializerMixin, viewsets.ModelViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorPermission, CommentPermission]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    