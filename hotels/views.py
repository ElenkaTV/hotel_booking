from rest_framework import viewsets, filters
from django.shortcuts import render, get_object_or_404
from django.db import models
from .models import Hotel, Room
from .serializers import HotelSerializer, RoomSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class HotelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'city']
    ordering_fields = ['stars', 'name']
    
    @swagger_auto_schema(
        operation_description="Получить список всех отелей",
        responses={200: HotelSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Получить детальную информацию об отеле по ID",
        responses={200: HotelSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

class RoomViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

def home(request):
    hotels = Hotel.objects.all()
    
    # Поиск по названию, городу или адресу (регистронезависимый)
    search_query = request.GET.get('search', '')
    if search_query:
        # Преобразуем поисковый запрос в нижний регистр
        search_lower = search_query.lower().strip()
        
        # Ручная фильтрация (работает с любым регистром)
        filtered_hotels = []
        for hotel in hotels:
            if (search_lower in hotel.name.lower() or 
                search_lower in hotel.city.lower() or 
                search_lower in hotel.address.lower()):
                filtered_hotels.append(hotel)
        hotels = filtered_hotels
    
    return render(request, 'hotels/home.html', {'hotels': hotels, 'search_query': search_query})

def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    rooms = hotel.rooms.all()
    return render(request, 'hotels/detail.html', {'hotel': hotel, 'rooms': rooms})