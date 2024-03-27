from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ChangePasswordView,
    UserAccountViewSet,
    UserLoginAPIView,
    UserLogoutAPIView,
    UserRegistrationAPIView,
    UserUpdateView,
    UserViewSet,
    activate,
)

router = DefaultRouter()
router.register("list", UserViewSet)
router.register("account", UserAccountViewSet)
urlpatterns = [
    path("", include(router.urls)),
    path("register/", UserRegistrationAPIView.as_view(), name="register"),
    path("login/", UserLoginAPIView.as_view(), name="login"),
    path("edit_profile/<int:pk>/", UserUpdateView.as_view(), name="edit_profile"),
    path("logout/", UserLogoutAPIView.as_view(), name="logout"),
    path("activate/<uid64>/<token>/", activate, name="activate"),
    path("change_password/<int:pk>/", ChangePasswordView.as_view(), name="change_pass"),
]
