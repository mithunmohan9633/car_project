from django import forms
from .models import CarForSale,CarForRent, OilType, Brand

class CarForSaleForm(forms.ModelForm):
    class Meta:
        model = CarForSale
        fields = ['name', 'model_year', 'km_driven', 'oil_type', 'accidental_background', 'description', 'price', 'mileage', 'front_image', 'leftside_img', 'rightside_img', 'back_image', 'registration_number', 'insurance_end_date', 'ownership_type']
class CarForSaleForm(forms.ModelForm):
    oil_type = forms.ChoiceField(choices=OilType.OIL_CHOICES, widget=forms.Select)
    brand = forms.CharField(max_length=100) 

    class Meta:
        model = CarForSale
        exclude = ['user']  

class CarForRentForm(forms.ModelForm):
    oil_type = forms.ChoiceField(choices=OilType.OIL_CHOICES, widget=forms.Select)
    brand = forms.CharField(max_length=100)

    class Meta:
        model = CarForRent
        exclude = ['user']
