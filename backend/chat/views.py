from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Room, Message
from .serializers import RoomSerializer
from .serializers import MessageSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class RoomListView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]

class RoomCreateView(generics.CreateAPIView):
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        room_id = self.kwargs["room_id"]
        return Message.objects.filter(room_id=room_id).order_by("timestamp")

    def perform_create(self, serializer):
        room_id = self.kwargs["room_id"]
        serializer.save(sender=self.request.user, room_id=room_id)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_messages(request):
    query = request.GET.get("q", "")
    messages = Message.objects.filter(content__icontains=query)
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)


