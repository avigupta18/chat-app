from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    RoomViewSet,
    MessageListCreateView,
    search_messages,
    NotificationViewSet,
)
router = DefaultRouter()
router.register(r"rooms", RoomViewSet, basename="room")
router.register(r"notifications", NotificationViewSet, basename="notification")
urlpatterns = [
    path("messages/<int:room_id>/", MessageListCreateView.as_view(), name="message-list"),
    path("messages/search/", search_messages, name="message-search"),
]
urlpatterns += router.urls