from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser, CarForRent, CarForSale, Brand, OilType
from .forms import CarForSaleForm, CarForRentForm
from django.contrib import messages
import random

# User Registration View
def user_registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        my_location_link = request.POST.get('my_location_link')
        profile_picture = request.FILES.get('profilepick')
        whatsapp_number = request.POST.get('whatsapp_num')

        user = CustomUser(
            username=username,
            email=email,
            phone=phone,
            my_location_link=my_location_link,
            profile_picture=profile_picture,
            whatsapp_number=whatsapp_number
        )
        user.set_password(password)
        user.save()
        login(request, user)
        return redirect('home')
    return render(request, 'signup.html')

# User Login View
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'login.html')
    return render(request, 'login.html')

# Home View
def home_view(request):
    return render(request, 'home.html')

# User Logout View
def user_logout(request):
    logout(request)
    return redirect('home')

# Add Car for Sale
@login_required
def add_car_for_sale(request):
    if request.method == 'POST':
        form = CarForSaleForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.user = request.user
            
            # Check if OilType exists or create it
            oil_type_value = form.cleaned_data['oil_type']
            oil_type, created = OilType.objects.get_or_create(type=oil_type_value)
            car.oil_type = oil_type
            
            # Check if Brand exists or create it
            brand_name = form.cleaned_data['brand']
            brand, created = Brand.objects.get_or_create(name=brand_name)
            car.brand = brand  # Ensure car.brand is assigned a Brand instance

            car.save()  # Save the car instance
            messages.success(request, "Congratulations! You have successfully added the car.")
            return redirect('home')  # Redirect to homepage after successful addition
    else:
        form = CarForSaleForm()
    
    # Fetch oil types to populate the dropdown
    oil_types = OilType.objects.all()
    return render(request, 'add_car_for_sale.html', {'form': form, 'oil_types': oil_types})
# List All Cars for Sale
@login_required
def list_cars_for_sale(request):
    cars = CarForSale.objects.all()  # Fetch all cars
    brand_filter = request.GET.get('brand')
    year_filter = request.GET.get('year')
    km_filter = request.GET.get('km_driven')
    oil_type_filter = request.GET.get('oil_type')
    price_filter = request.GET.get('price')
    search_query = request.GET.get('search')

    if brand_filter:
        cars = cars.filter(brand__name=brand_filter)
    if year_filter:
        if year_filter == 'below_3':
            cars = cars.filter(model_year__gte=2021)  # Assuming the current year is 2024
        elif year_filter == '3_to_5':
            cars = cars.filter(model_year__gte=2019, model_year__lt=2021)
        elif year_filter == '5_to_10':
            cars = cars.filter(model_year__gte=2014, model_year__lt=2019)
        elif year_filter == 'above_10':
            cars = cars.filter(model_year__lt=2014)
    if km_filter:
        if km_filter == 'below_10k':
            cars = cars.filter(km_driven__lt=10000)
        elif km_filter == '10k_to_20k':
            cars = cars.filter(km_driven__gte=10000, km_driven__lt=20000)
        elif km_filter == '20k_to_40k':
            cars = cars.filter(km_driven__gte=20000, km_driven__lt=40000)
        elif km_filter == 'above_40k':
            cars = cars.filter(km_driven__gte=40000)
    if oil_type_filter:
        cars = cars.filter(oil_type__type=oil_type_filter)
    if price_filter:
        if price_filter == 'below_50k':
            cars = cars.filter(price__lt=50000)
        elif price_filter == '1L_to_3L':
            cars = cars.filter(price__gte=100000, price__lt=300000)
        elif price_filter == '3L_to_5L':
            cars = cars.filter(price__gte=300000, price__lt=500000)
        elif price_filter == '5L_to_10L':
            cars = cars.filter(price__gte=500000, price__lt=1000000)
        elif price_filter == 'above_10L':
            cars = cars.filter(price__gte=1000000)
    if search_query:
        cars = cars.filter(name__icontains=search_query)

    # Fetching filter options
    brands = Brand.objects.all()
    oil_types = OilType.objects.all()

    return render(request, 'list_cars_for_sale.html', {'cars': cars, 'brands': brands, 'oil_types': oil_types})

# List User's Cars for Sale
@login_required
def list_my_cars(request):
    my_cars = CarForSale.objects.filter(user=request.user)  # Fetch cars by logged-in user
    return render(request, 'list_my_cars.html', {'my_cars': my_cars})

# Add Car for Rent
@login_required
def add_car_for_rent(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        brand_name = request.POST.get('brand')
        oil_type_name = request.POST.get('oil_type')
        description = request.POST.get('description')
        price_per_day = request.POST.get('price_per_day')
        mileage = request.POST.get('mileage')
        rent_car_image = request.FILES.get('rent_car_image')

        # Ensure that the required fields are filled
        if not rent_car_image:
            return render(request, 'add_car_for_rent.html', {'error': 'Please upload a car image.'})

        # Create or retrieve the brand instance based on the provided text input
        brand, created = Brand.objects.get_or_create(name=brand_name)
        oil_type, created = OilType.objects.get_or_create(type=oil_type_name)

        # Create the CarForRent instance
        car_rent = CarForRent(
            user=request.user,
            name=name,
            brand=brand,
            oil_type=oil_type,
            description=description,
            price_per_day=price_per_day,
            mileage=mileage,
            rent_car_image=rent_car_image,
        )
        car_rent.save()

        return redirect('list_my_rent_cars')

    context = {}
    return render(request, 'add_car_for_rent.html', context)

# List All Cars for Rent
@login_required
def list_cars_for_rent(request):
    cars_for_rent = CarForRent.objects.all()
    brand_filter = request.GET.get('brand')
    oil_type_filter = request.GET.get('oil_type')
    price_filter = request.GET.get('price')
    search_query = request.GET.get('search')

    if brand_filter:
        cars_for_rent = cars_for_rent.filter(brand__name=brand_filter)
    if oil_type_filter:
        cars_for_rent = cars_for_rent.filter(oil_type__type=oil_type_filter)
    if price_filter:
        if price_filter == 'below_50k':
            cars_for_rent = cars_for_rent.filter(price_per_day__lt=50000)
        elif price_filter == '1L_to_3L':
            cars_for_rent = cars_for_rent.filter(price_per_day__gte=100000, price_per_day__lt=300000)
        elif price_filter == '3L_to_5L':
            cars_for_rent = cars_for_rent.filter(price_per_day__gte=300000, price_per_day__lt=500000)
        elif price_filter == '5L_to_10L':
            cars_for_rent = cars_for_rent.filter(price_per_day__gte=500000, price_per_day__lt=1000000)
        elif price_filter == 'above_10L':
            cars_for_rent = cars_for_rent.filter(price_per_day__gte=1000000)
    if search_query:
        cars_for_rent = cars_for_rent.filter(name__icontains=search_query)

    # Fetching filter options
    brands = Brand.objects.all()
    oil_types = OilType.objects.all()

    return render(request, 'list_cars_for_rent.html', {'cars_for_rent': cars_for_rent, 'brands': brands, 'oil_types': oil_types})

# List User's Cars for Rent
@login_required
def list_my_rent_cars(request):
    my_rent_cars = CarForRent.objects.filter(user=request.user)
    return render(request, 'list_my_rent_cars.html', {'my_rent_cars': my_rent_cars})

# Car for Sale Detail View
def car_for_sale_detail(request, car_id):
    car = get_object_or_404(CarForSale, id=car_id)
    all_cars = list(CarForSale.objects.exclude(id=car.id))
    random_cars = random.sample(all_cars, min(10, len(all_cars)))
    return render(request, 'car_for_sale_detail.html', {'car': car, 'random_cars': random_cars})

# Car for Rent Detail View
def car_for_rent_detail(request, car_id):
    car = get_object_or_404(CarForRent, id=car_id)
    all_cars = list(CarForRent.objects.exclude(id=car.id))
    random_cars = random.sample(all_cars, min(10, len(all_cars)))
    return render(request, 'car_for_rent_detail.html', {'car': car, 'random_cars': random_cars})

# Edit Car for Sale (only by owner)
@login_required
def car_for_sale_edit(request, car_id):
    car = get_object_or_404(CarForSale, id=car_id, user=request.user)
    if request.method == 'POST':
        form = CarForSaleForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            car = form.save(commit=False)

            oil_type_value = form.cleaned_data['oil_type']
            oil_type, created = OilType.objects.get_or_create(type=oil_type_value)
            car.oil_type = oil_type

            brand_name = form.cleaned_data['brand']
            brand, created = Brand.objects.get_or_create(name=brand_name)
            car.brand = brand

            car.save()
            return redirect('car_for_sale_detail', car_id=car.id)
    else:
        form = CarForSaleForm(instance=car)

    return render(request, 'edit_car_for_sale.html', {'form': form, 'car': car})

# Edit Car for Rent (only by owner)
@login_required
def car_for_rent_edit(request, car_id):
    car = get_object_or_404(CarForRent, id=car_id, user=request.user)
    if request.method == 'POST':
        name = request.POST.get('name')
        brand_name = request.POST.get('brand')
        oil_type_name = request.POST.get('oil_type')
        description = request.POST.get('description')
        price_per_day = request.POST.get('price_per_day')
        mileage = request.POST.get('mileage')
        rent_car_image = request.FILES.get('rent_car_image')

        car.name = name
        car.brand, _ = Brand.objects.get_or_create(name=brand_name)
        car.oil_type, _ = OilType.objects.get_or_create(type=oil_type_name)
        car.description = description
        car.price_per_day = price_per_day
        car.mileage = mileage
        if rent_car_image:
            car.rent_car_image = rent_car_image
        car.save()

        return redirect('car_for_rent_detail', car_id=car.id)
    return render(request, 'edit_car_for_rent.html', {'car': car})

# Delete Car for Sale (only by owner)
@login_required
def delete_car_for_sale(request, car_id):
    car = get_object_or_404(CarForSale, id=car_id, user=request.user)
    if request.method == 'POST':
        car.delete()
        return redirect('list_cars_for_sale')
    return render(request, 'confirm_delete.html', {'car': car})

# Delete Car for Rent (only by owner)
@login_required
def delete_car_for_rent(request, car_id):
    car = get_object_or_404(CarForRent, id=car_id, user=request.user)
    if request.method == 'POST':
        car.delete()
        return redirect('list_cars_for_rent')
    return render(request, 'confirm_delete.html', {'car': car})
def car_for_rent_edit(request, car_id):
    car = get_object_or_404(CarForRent, id=car_id, user=request.user)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        brand_name = request.POST.get('brand')
        oil_type_name = request.POST.get('oil_type')
        description = request.POST.get('description')
        price_per_day = request.POST.get('price_per_day')
        mileage = request.POST.get('mileage')
        rent_car_image = request.FILES.get('rent_car_image')

        # Update car fields
        car.name = name
        car.brand, _ = Brand.objects.get_or_create(name=brand_name)
        car.oil_type, _ = OilType.objects.get_or_create(type=oil_type_name)
        car.description = description
        car.price_per_day = price_per_day
        car.mileage = mileage
        
        if rent_car_image:
            car.rent_car_image = rent_car_image
        
        car.save()
        messages.success(request, 'Car details updated successfully!')
        return redirect('car_for_rent_detail', car_id=car.id)

    # If the request method is GET, we render the edit form with the current car details
    return render(request, 'edit_car_for_rent.html', {'car': car})
