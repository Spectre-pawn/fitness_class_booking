from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils import timezone
from .models import FitnessClass, Booking

@admin.register(FitnessClass)
class FitnessClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'datetime', 'instructor', 'available_slots', 'total_slots', 'is_upcoming']
    list_filter = ['name', 'instructor', 'datetime']
    search_fields = ['name', 'instructor']
    ordering = ['datetime']
    
    def is_upcoming(self, obj):
        return obj.is_upcoming()
    is_upcoming.boolean = True

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'client_email', 'fitness_class', 'booking_time']
    list_filter = ['fitness_class__name', 'booking_time']
    search_fields = ['client_name', 'client_email', 'fitness_class__name']
    ordering = ['-booking_time']
