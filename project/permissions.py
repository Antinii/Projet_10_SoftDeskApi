from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from project.models import Contributor


def is_contributor(user, project):
    """
    Checks if the user is a contributor of the project.
    """
    if Contributor.objects.filter(user=user, project=project).exists():
        return True
    else:
        raise PermissionDenied(
                    "Seul un contributeur peut effectuer cette action"
                )


class IsAuthorPermission(permissions.BasePermission):
    """
    Permission class to check if the user is the author of an object.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in ["PUT", "DELETE", "PATCH"]:
            if obj.author == request.user:
                return True
            else:
                raise PermissionDenied(
                    "Seul l'auteur peut effectuer cette action"
                )
        return True


class ProjectPermission(permissions.BasePermission):
    """
    Permission class to check if the user has permission for project-related actions.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return is_contributor(request.user, obj.id)
        return True


class ContributorPermission(permissions.BasePermission):
    """
    Permission class to check if the user has permission for contributor-related actions.
    """
    def has_object_permission(self, request, view, obj):
        project = obj.project
        if request.method == "DELETE":
            if project.author == request.user:
                return True
            else:
                raise PermissionDenied(
                    "Seul l'auteur du projet peut supprimer un contributeur."
                )
        else:
            return is_contributor(request.user, project)


class IssuePermission(permissions.BasePermission):
    """
    Permission class to check if the user has permission for issue-related actions.
    """
    def has_object_permission(self, request, view, obj):
        return is_contributor(request.user, obj.project)


class CommentPermission(permissions.BasePermission):
    """
    Permission class to check if the user has permission for comment-related actions.
    """
    def has_object_permission(self, request, view, obj):
        return is_contributor(request.user, obj.issue.project)
