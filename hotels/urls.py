from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'hotels', views.HotelViewSet)
router.register(r'rooms', views.RoomViewSet)

urlpatterns = [
    path('', include(router.urls)),
]