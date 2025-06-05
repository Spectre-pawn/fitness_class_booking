from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
from .models import FitnessClass, Booking
from .serializers import FitnessClassSerializer, BookingSerializer, BookingCreateSerializer
import logging

logger = logging.getLogger('booking')

@api_view(['GET'])
def list_classes(request):
    # Returns a list of all upcoming fitness classes
    # Optional query parameters:
    # - timezone: Convert datetime to specified timezone (e.g., ?timezone=America/New_York)
   
    try:
        # Filter only upcoming classes
        upcoming_classes = FitnessClass.objects.filter(
            datetime__gt=timezone.now(),
            available_slots__gt=0
        )
        
        serializer = FitnessClassSerializer(
            upcoming_classes, 
            many=True, 
            context={'request': request}
        )
        
        logger.info(f"Retrieved {len(upcoming_classes)} upcoming classes")
        
        return Response({
            'success': True,
            'data': serializer.data,
            'count': len(upcoming_classes)
        })
        
    except Exception as e:
        logger.error(f"Error retrieving classes: {str(e)}")
        return Response({
            'success': False,
            'error': 'Internal server error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def create_booking(request):

    # Create a new booking for a fitness class
    # Required fields: class_id, client_name, client_email
 
    try:
        serializer = BookingCreateSerializer(data=request.data)
        
        if not serializer.is_valid():
            logger.warning(f"Invalid booking data: {serializer.errors}")
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        
        # Use transaction to ensure data consistency
        with transaction.atomic():
            try:
                fitness_class = FitnessClass.objects.select_for_update().get(
                    id=validated_data['class_id']
                )
                
                # Double-check availability (race condition protection)
                if fitness_class.available_slots <= 0:
                    return Response({
                        'success': False,
                        'error': 'No available slots for this class'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # Create booking
                booking = Booking.objects.create(
                    fitness_class=fitness_class,
                    client_name=validated_data['client_name'],
                    client_email=validated_data['client_email']
                )
                
                # Reduce available slots
                fitness_class.available_slots -= 1
                fitness_class.save()
                
                booking_serializer = BookingSerializer(booking)
                
                logger.info(f"Booking created: {booking.client_email} for class {fitness_class.name}")
                
                return Response({
                    'success': True,
                    'message': 'Booking created successfully',
                    'data': booking_serializer.data
                }, status=status.HTTP_201_CREATED)
                
            except FitnessClass.DoesNotExist:
                return Response({
                    'success': False,
                    'error': 'Class not found'
                }, status=status.HTTP_404_NOT_FOUND)
                
    except Exception as e:
        logger.error(f"Error creating booking: {str(e)}")
        return Response({
            'success': False,
            'error': 'Internal server error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def list_bookings(request):
   
    # Returns all bookings for a specific email address
    # Required query parameter: email
  
    try:
        client_email = request.query_params.get('email')
        
        if not client_email:
            return Response({
                'success': False,
                'error': 'Email parameter is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        bookings = Booking.objects.filter(client_email=client_email)
        serializer = BookingSerializer(bookings, many=True)
        
        logger.info(f"Retrieved {len(bookings)} bookings for {client_email}")
        
        return Response({
            'success': True,
            'data': serializer.data,
            'count': len(bookings)
        })
        
    except Exception as e:
        logger.error(f"Error retrieving bookings: {str(e)}")
        return Response({
            'success': False,
            'error': 'Internal server error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
