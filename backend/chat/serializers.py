from rest_framework import serializers
from .models import Room
from .models import Message

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"
        read_only_fields = ("id", "created_by", "created_at")



class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source="sender.username", read_only=True)

    class Meta:
        model = Message
        fields = "__all__"
        read_only_fields = ("id", "sender", "timestamp")
