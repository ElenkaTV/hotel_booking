from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['user', 'total_price', 'created_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        room = validated_data['room']
        nights = (validated_data['check_out'] - validated_data['check_in']).days
        validated_data['total_price'] = room.price_per_night * nights
        return super().create(validated_data)