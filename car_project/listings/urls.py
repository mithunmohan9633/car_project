from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('signup/', views.user_registration, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('add-car-for-sale/', views.add_car_for_sale, name='add_car_for_sale'),
    path('list-my-cars/', views.list_my_cars, name='list_my_cars'),
    path('list-cars-for-sale/', views.list_cars_for_sale, name='list_cars_for_sale'),
    path('add-car-for-rent/', views.add_car_for_rent, name='add_car_for_rent'),
    path('list-my-rent-cars/', views.list_my_rent_cars, name='list_my_rent_cars'),
    path('list-cars-for-rent/', views.list_cars_for_rent, name='list_cars_for_rent'),
    path('cars-for-rent/<int:car_id>/', views.car_for_rent_detail, name='car_for_rent_detail'),
    path('car-for-sale/<int:car_id>/', views.car_for_sale_detail, name='car_for_sale_detail'),
    path('delete-car-for-sale/<int:car_id>/', views.delete_car_for_sale, name='delete_car_for_sale'),
    path('delete-car-for-rent/<int:car_id>/', views.delete_car_for_rent, name='delete_car_for_rent'),
    path('cars-for-sale/edit/<int:car_id>/', views.car_for_sale_edit, name='edit_my_car_for_sale'), 
    path('cars-for-rent/edit/<int:car_id>/', views.car_for_rent_edit, name='edit_my_rent_car'),
    # Add more paths as needed
]
