from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date, timedelta
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Booking
from .serializers import BookingSerializer
from hotels.models import Room, Hotel
from .forms import BookingForm
from drf_yasg.utils import swagger_auto_schema

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
    
    @swagger_auto_schema(
        operation_description="Создать новое бронирование",
        responses={201: BookingSerializer(), 400: "Ошибка валидации"}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Получить список бронирований текущего пользователя",
        responses={200: BookingSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Отменить бронирование",
        responses={200: "Статус отмены"}
    )
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        booking.status = 'cancelled'
        booking.save()
        return Response({'status': 'cancelled', 'message': 'Бронирование отменено'})@login_required
@login_required
def create_booking(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.room = room
            
            # Рассчитываем количество ночей и общую цену
            nights = (booking.check_out - booking.check_in).days
            booking.total_price = room.price_per_night * nights
            booking.status = 'confirmed'
            
            # Проверка на конфликт дат
            conflicting = Booking.objects.filter(
                room=room,
                status__in=['pending', 'confirmed'],
                check_in__lt=booking.check_out,
                check_out__gt=booking.check_in
            )
            
            if conflicting.exists():
                messages.error(request, 'Номер уже забронирован на выбранные даты')
                return render(request, 'bookings/create.html', {'room': room, 'form': form})
            
            booking.save()
            messages.success(request, f'Бронирование успешно создано! Сумма: {booking.total_price} ₽')
            return redirect('my_bookings')
        else:
            # Если форма не валидна, показываем ошибки
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
    else:
        form = BookingForm()
    
    return render(request, 'bookings/create.html', {'room': room, 'form': form})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'bookings/my_bookings.html', {
        'bookings': bookings,
        'today': date.today()  # <-- ДЛЯ ПРОВЕРКИ ДАТЫ В ШАБЛОНЕ
    })
@login_required
def cancel_booking(request, booking_id):
    from datetime import date
    from django.contrib import messages
    from django.shortcuts import get_object_or_404, redirect
    
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.status != 'confirmed':
        messages.error(request, 'Это бронирование нельзя отменить')
        return redirect('my_bookings')
    
    # Проверка: можно отменить только за 24 часа до заезда
    now = date.today()
    days_until_checkin = (booking.check_in - now).days
    
    if days_until_checkin < 1:
        messages.error(request, '❌ Отмена невозможна: до заезда осталось менее 24 часов')
    else:
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, f'✅ Бронирование #{booking.id} успешно отменено')
    
    return redirect('my_bookings')