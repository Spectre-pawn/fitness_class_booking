from rest_framework import serializers
from django.utils import timezone
from .models import FitnessClass, Booking
import pytz

class FitnessClassSerializer(serializers.ModelSerializer):
    datetime_local = serializers.SerializerMethodField()
    
    class Meta:
        model = FitnessClass
        fields = ['id', 'name', 'datetime', 'datetime_local', 'instructor', 'available_slots', 'total_slots']
        read_only_fields = ['id']
    
    def get_datetime_local(self, obj):
        """Return datetime in the requested timezone or IST by default"""
        request = self.context.get('request')
        if request and 'timezone' in request.query_params:
            try:
                tz = pytz.timezone(request.query_params['timezone'])
                return obj.get_datetime_in_timezone(tz).isoformat()
            except pytz.exceptions.UnknownTimeZoneError:
                pass
        return obj.datetime.isoformat()

class BookingSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source='fitness_class.name', read_only=True)
    class_datetime = serializers.DateTimeField(source='fitness_class.datetime', read_only=True)
    instructor = serializers.CharField(source='fitness_class.instructor', read_only=True)
    
    class Meta:
        model = Booking
        fields = ['id', 'class_name', 'class_datetime', 'instructor', 'client_name', 'client_email', 'booking_time']
        read_only_fields = ['id', 'booking_time']

class BookingCreateSerializer(serializers.Serializer):
    class_id = serializers.IntegerField()
    client_name = serializers.CharField(max_length=100)
    client_email = serializers.EmailField()
    
    def validate_class_id(self, value):
        """Validate that the class exists and is upcoming"""
        try:
            fitness_class = FitnessClass.objects.get(id=value)
        except FitnessClass.DoesNotExist:
            raise serializers.ValidationError("Class not found.")
        
        if not fitness_class.is_upcoming():
            raise serializers.ValidationError("Cannot book past classes.")
        
        if fitness_class.available_slots <= 0:
            raise serializers.ValidationError("No available slots for this class.")
        
        return value
    
    def validate(self, data):
        """Check for duplicate bookings"""
        try:
            fitness_class = FitnessClass.objects.get(id=data['class_id'])
            if Booking.objects.filter(
                fitness_class=fitness_class,
                client_email=data['client_email']
            ).exists():
                raise serializers.ValidationError("You have already booked this class.")
        except FitnessClass.DoesNotExist:
            pass  # Will be caught by validate_class_id
        
        return data