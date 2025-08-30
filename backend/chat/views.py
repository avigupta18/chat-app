# chat/views.py
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Room, Message, Notification
from .serializers import RoomSerializer, MessageSerializer, NotificationSerializer


# ROOMS (list/create/retrieve)
class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Room.objects.none()
        return Room.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)



class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Message.objects.none()
        room_id = self.kwargs["room_id"]
        return Message.objects.filter(room_id=room_id).order_by("timestamp")

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user, room_id=self.kwargs["room_id"])


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_messages(request):
    q = request.GET.get("q", "")
    qs = Message.objects.filter(content__icontains=q).order_by("-timestamp")
    return Response(MessageSerializer(qs, many=True).data)



class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Notification.objects.none()
        return Notification.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        if getattr(self, "swagger_fake_view", False):
            return None
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        return Response({"detail": "Deleting notifications is not allowed."},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)
