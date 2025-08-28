from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Room, Message, Notification
from .serializers import RoomSerializer, MessageSerializer, NotificationSerializer, UserSerializer
from users.models import User

class RoomListView(generics.ListAPIView):
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Room.objects.none()
        return Room.objects.all()
    
class RoomCreateView(generics.CreateAPIView):
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class RoomDetailView(generics.RetrieveAPIView):
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Room.objects.none()
        return Room.objects.all()

class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Message.objects.none()
        room_id = self.kwargs["room_id"]
        return Message.objects.filter(room_id=room_id).order_by("timestamp")
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user, room_id=self.kwargs["room_id"])
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_messages(request):
    query = request.GET.get("q", "")
    messages = Message.objects.filter(content__icontains=query)
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Notification.objects.none()
        return Notification.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return User.objects.none()
        return User.objects.all()
    @action(detail=True, methods=["post"])
    def ban(self, request, pk=None):
        if getattr(self, 'swagger_fake_view', False):
            return Response({"status": "swagger placeholder"})
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({"status": f"User {user.username} banned"})