from rest_framework import viewsets, status
from rest_framework.views import APIView
from authentication.serializer import UserSerializer, SignupSerializer
from authentication.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling CRUD operations on user accounts.
    Inherits from viewsets.ModelViewSet.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        """
        Updates an existing user account.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if request.user == instance:
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return Response({"message": "You do not have permission to update this user."},
                            status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        """
        Deletes an existing user account.
        Checks if the user making the request is the owner of the user account.
        If they match, deletes the user account.
        Otherwise, returns a 403 Forbidden response.
        """
        instance = self.get_object()

        if request.user == instance:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "You do not have permission to delete this user."},
                            status=status.HTTP_403_FORBIDDEN)


class SignupView(APIView):
    """
    View to create a user
    """

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
