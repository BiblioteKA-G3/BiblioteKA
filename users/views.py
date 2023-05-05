from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied

from users.models import User
from users.serializers import UserSerializer
from users.permissions import IsAccountEmployee


class UserView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied()
        return super().get(request, *args, **kwargs)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountEmployee]

    queryset = User.objects.all()
    serializer_class = UserSerializer
