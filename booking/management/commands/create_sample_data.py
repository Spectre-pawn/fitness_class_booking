from django.core.management.base import BaseCommand
from django.utils import timezone
from booking.models import FitnessClass
from datetime import timedelta

class Command(BaseCommand):
    help = 'Create sample fitness classes'
    
    def handle(self, *args, **options):
        classes_data = [
            {
                'name': 'YOGA',
                'instructor': 'Pawan shejwal',
                'total_slots': 15,
                'hours_from_now': 2
            },
            {
                'name': 'ZUMBA',
                'instructor': 'Ganesh Katore',
                'total_slots': 20,
                'hours_from_now': 4
            },
            {
                'name': 'HIIT',
                'instructor': 'Deepak Thakur',
                'total_slots': 12,
                'hours_from_now': 6
            },
            {
                'name': 'YOGA',
                'instructor': 'Gokul Katore',
                'total_slots': 15,
                'hours_from_now': 26 # This class is scheduled for the next day
            }
        ]
        
        for class_data in classes_data:
            datetime = timezone.now() + timedelta(hours=class_data['hours_from_now'])
            
            fitness_class, created = FitnessClass.objects.get_or_create(
                name=class_data['name'],
                datetime=datetime,
                instructor=class_data['instructor'],
                defaults={
                    'total_slots': class_data['total_slots'],
                    'available_slots': class_data['total_slots']
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created class: {fitness_class.name} - {fitness_class.datetime}'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'Class already exists: {fitness_class.name} - {fitness_class.datetime}'
                    )
                )
