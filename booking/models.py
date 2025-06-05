from django.db import models
from django.core.validators import MinValueValidator, EmailValidator
from django.utils import timezone
import pytz

class FitnessClass(models.Model):
    CLASS_TYPES = [
        ('YOGA', 'Yoga'),
        ('ZUMBA', 'Zumba'),
        ('HIIT', 'HIIT'),
    ]
    
    name = models.CharField(max_length=100, choices=CLASS_TYPES)
    datetime = models.DateTimeField()
    instructor = models.CharField(max_length=100)
    total_slots = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    available_slots = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['datetime']
    
    def __str__(self):
        return f"{self.name} - {self.datetime.strftime('%Y-%m-%d %H:%M')} - {self.instructor}"
    
    def save(self, *args, **kwargs):
        # Ensure available_slots doesn't exceed total_slots
        if self.available_slots > self.total_slots:
            self.available_slots = self.total_slots
        super().save(*args, **kwargs)
    
    def is_upcoming(self):
        """Check if the class is in the future"""
        return self.datetime > timezone.now()
    
    def get_datetime_in_timezone(self, target_timezone):
        """Convert datetime to specified timezone"""
        if isinstance(target_timezone, str):
            target_timezone = pytz.timezone(target_timezone)
        return self.datetime.astimezone(target_timezone)

class Booking(models.Model):
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE, related_name='bookings')
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField(validators=[EmailValidator()])
    booking_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['fitness_class', 'client_email']
        ordering = ['-booking_time']
    
    def __str__(self):
        return f"{self.client_name} - {self.fitness_class.name} - {self.fitness_class.datetime.strftime('%Y-%m-%d %H:%M')}"
