from django.contrib import admin
from django.urls import path, include
from users.views import RegisterView, MeView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
schema_view = get_schema_view(
    openapi.Info(
        title="Chat API",
        default_version="v1",
        description="API documentation for Chat Application",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", TokenObtainPairView.as_view(), name="login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("users/me/", MeView.as_view(), name="me"),
    path("api/", include("chat.urls")),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="redoc"),
]
