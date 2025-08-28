from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    RoomListView,
    RoomCreateView,
    RoomDetailView,
    MessageListCreateView,
    search_messages,
    NotificationViewSet,
    UserViewSet,
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path("rooms/", RoomListView.as_view(), name="room-list"),
    path("rooms/create/", RoomCreateView.as_view(), name="room-create"),
    path("rooms/<int:pk>/", RoomDetailView.as_view(), name="room-detail"),
    path("messages/<int:room_id>/", MessageListCreateView.as_view(), name="message-list"),
    path("messages/search/", search_messages, name="message-search"),
]
urlpatterns += router.urls





