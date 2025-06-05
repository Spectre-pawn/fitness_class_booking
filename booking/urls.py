from django.urls import path
from . import views

urlpatterns = [
    path('classes/', views.list_classes, name='list_classes'),
    path('book/', views.create_booking, name='create_booking'),
    path('bookings/', views.list_bookings, name='list_bookings'),
]