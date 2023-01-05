from .serializers import UserProfileSerializer

from user.models import UserProfile

from rest_framework import viewsets, permissions, status
from .permissions import IsOwnerOrReadOnly


class UserProfileViewSet(viewsets.ModelViewSet):

    queryset = UserProfile.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = UserProfileSerializer