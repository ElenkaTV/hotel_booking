from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from hotels.models import Hotel
from .models import Review
from .forms import ReviewForm

@login_required
def add_review(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    
    # Проверка: пользователь уже оставлял отзыв?
    existing_review = Review.objects.filter(user=request.user, hotel=hotel).first()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.hotel = hotel
            review.save()
            messages.success(request, 'Спасибо за ваш отзыв!')
            return redirect('hotel_detail', hotel_id=hotel.id)
    else:
        form = ReviewForm(instance=existing_review)
    
    return render(request, 'reviews/add_review.html', {
        'hotel': hotel,
        'form': form,
        'existing_review': existing_review
    })