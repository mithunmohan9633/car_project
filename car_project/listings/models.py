from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Ensure email is unique
    phone = models.CharField(max_length=15, unique=True)  # Unique phone number
    my_location_link = models.URLField(blank=True, null=True)  
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True) 
    whatsapp_number = models.CharField(max_length=15, blank=True, null=True)  

    def __str__(self):
        return self.username

class OilType(models.Model):
    OIL_CHOICES = [
        ('Petrol', 'Petrol'),
        ('Diesel', 'Diesel'),
        ('Electric', 'Electric'),
    ]
    type = models.CharField(max_length=10, choices=OIL_CHOICES, unique=True)

    def __str__(self):
        return self.type

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True) 

    def __str__(self):
        return self.name

class CarForSale(models.Model):
    OWNERSHIP_CHOICES = [
        ('1st', '1st Owner'),
        ('2nd', '2nd Owner'),
        ('3rd', '3rd Owner'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    model_year = models.IntegerField()
    km_driven = models.IntegerField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    oil_type = models.ForeignKey(OilType, on_delete=models.CASCADE)
    accidental_background = models.BooleanField(default=False)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    mileage = models.DecimalField(max_digits=5, decimal_places=2)  
    front_image = models.ImageField(upload_to='car_images/', blank=True, null=True)
    leftside_img = models.ImageField(upload_to='car_images/', blank=True, null=True)
    rightside_img = models.ImageField(upload_to='car_images/', blank=True, null=True)
    back_image = models.ImageField(upload_to='car_images/', blank=True, null=True)

    registration_number = models.CharField(max_length=20, unique=True)  
    insurance_end_date = models.DateField()  
    ownership_type = models.CharField(max_length=10, choices=OWNERSHIP_CHOICES)
    created_date = models.DateField(auto_now_add=True) 
    created_time = models.TimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.name} - {self.user.username}"

class CarForRent(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
    name = models.CharField(max_length=100) 
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)  
    oil_type = models.ForeignKey(OilType, on_delete=models.CASCADE)
    description = models.TextField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    mileage = models.DecimalField(max_digits=5, decimal_places=2)  
    rent_car_image = models.ImageField(upload_to='car_images/rent_car_images', blank=True, null=True)
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.name} - {self.user.username}"
