from rest_framework import viewsets
from rest_framework.views import APIView
from authentication.serializer import UserSerializer, SignupSerializer
from authentication.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    

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
