from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from comment.models import Comment
from project.permissions import IsAuthorPermission, CommentPermission
from comment.serializers import CommentListSerializer, CommentDetailSerializer
from project.views import MultipleSerializerMixin


class CommentViewSet(MultipleSerializerMixin, viewsets.ModelViewSet):

    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer
    permission_classes = [IsAuthenticated, IsAuthorPermission, CommentPermission]

    def get_queryset(self):
        project_id = self.kwargs.get('project_pk')
        issue_id = self.kwargs.get('issue_pk')
        queryset = Comment.objects.filter(issue__project_id=project_id, issue_id=issue_id)
        return queryset

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return self.detail_serializer_class
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
