from rest_framework import serializers
from .models import Room, Message, Notification
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "is_active", "is_staff", "avatar", "status"]

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "name", "created_by", "created_at"]
        read_only_fields = ["id", "created_by", "created_at"]

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "room", "sender", "content", "file", "timestamp"]
        read_only_fields = ["id", "sender", "timestamp"]

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "user", "message", "text", "is_read", "created_at"]
        read_only_fields = ["id", "user", "created_at"]
