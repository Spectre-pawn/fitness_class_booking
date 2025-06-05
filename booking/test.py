
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from .models import FitnessClass, Booking
import pytz
from datetime import timedelta

class FitnessClassModelTest(TestCase):
    def setUp(self):
        self.future_time = timezone.now() + timedelta(hours=2)
        self.fitness_class = FitnessClass.objects.create(
            name='YOGA',
            datetime=self.future_time,
            instructor='John Doe',
            total_slots=10,
            available_slots=10
        )
    
    def test_is_upcoming(self):
        self.assertTrue(self.fitness_class.is_upcoming())
        
        # Test past class
        past_class = FitnessClass.objects.create(
            name='HIIT',
            datetime=timezone.now() - timedelta(hours=1),
            instructor='Jane Doe',
            total_slots=5,
            available_slots=5
        )
        self.assertFalse(past_class.is_upcoming())
    
    def test_timezone_conversion(self):
        utc_time = self.fitness_class.get_datetime_in_timezone('UTC')
        self.assertIsNotNone(utc_time)

class BookingAPITest(APITestCase):
    def setUp(self):
        self.future_time = timezone.now() + timedelta(hours=2)
        self.fitness_class = FitnessClass.objects.create(
            name='YOGA',
            datetime=self.future_time,
            instructor='John Doe',
            total_slots=2,
            available_slots=2
        )
    
    def test_list_classes(self):
        url = reverse('list_classes')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(len(response.data['data']), 1)
    
    def test_create_booking_success(self):
        url = reverse('create_booking')
        data = {
            'class_id': self.fitness_class.id,
            'client_name': 'Test Client',
            'client_email': 'test@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        
        # Check if available slots reduced
        self.fitness_class.refresh_from_db()
        self.assertEqual(self.fitness_class.available_slots, 1)
    
    def test_create_booking_duplicate(self):
        # Create first booking
        Booking.objects.create(
            fitness_class=self.fitness_class,
            client_name='Test Client',
            client_email='test@example.com'
        )
        
        # Try to create duplicate booking
        url = reverse('create_booking')
        data = {
            'class_id': self.fitness_class.id,
            'client_name': 'Test Client',
            'client_email': 'test@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_booking_no_slots(self):
        # Fill all slots
        self.fitness_class.available_slots = 0
        self.fitness_class.save()
        
        url = reverse('create_booking')
        data = {
            'class_id': self.fitness_class.id,
            'client_name': 'Test Client',
            'client_email': 'test@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_list_bookings(self):
        # Create a booking
        booking = Booking.objects.create(
            fitness_class=self.fitness_class,
            client_name='Test Client',
            client_email='test@example.com'
        )
        
        url = reverse('list_bookings')
        response = self.client.get(url, {'email': 'test@example.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(len(response.data['data']), 1)
    
    def test_list_bookings_no_email(self):
        url = reverse('list_bookings')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
