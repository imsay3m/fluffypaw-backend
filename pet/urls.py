from django.urls import include, path
from rest_framework.routers import DefaultRouter

from transaction.views import AdoptPetAPIView

from .views import CategoryViewSet, PetViewSet, ReviewViewSet

# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register("list", PetViewSet)
router.register("category", CategoryViewSet)
router.register("review", ReviewViewSet)
urlpatterns = [
    path("", include(router.urls)),
    path("adopt/", AdoptPetAPIView.as_view()),
]
