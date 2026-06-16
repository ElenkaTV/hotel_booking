from django import forms
from .models import Booking
from datetime import date

class BookingForm(forms.ModelForm):
    check_in = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Дата заезда'
    )
    check_out = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Дата выезда'
    )
    guests = forms.IntegerField(
        min_value=1, 
        max_value=10, 
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label='Количество гостей'
    )
    
    class Meta:
        model = Booking
        fields = ['check_in', 'check_out', 'guests']
    
    def clean_check_in(self):
        check_in = self.cleaned_data.get('check_in')
        if check_in and check_in < date.today():
            raise forms.ValidationError('Дата заезда не может быть в прошлом')
        return check_in
    
    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')
        
        if check_in and check_out:
            if check_in >= check_out:
                raise forms.ValidationError('Дата выезда должна быть позже даты заезда')
            
            if check_in == check_out:
                raise forms.ValidationError('Дата заезда и выезда не могут совпадать (минимум 1 ночь)')
        
        return cleaned_data