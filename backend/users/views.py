from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, UserSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "status": getattr(user, "status", ""),
            "avatar": user.avatar.url if getattr(user, "avatar", None) else None,
        })



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


    def create(self, request, *args, **kwargs):
        return Response({"detail": "Use /auth/register/ instead."},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


    def destroy(self, request, *args, **kwargs):
        return Response({"detail": "User deletion not allowed."},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=True, methods=["post"])
    def ban(self, request, pk=None):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({"status": f"User {user.username} has been banned."})
