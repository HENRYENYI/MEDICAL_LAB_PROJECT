from django.core.management.base import BaseCommand
from consultation.models import ConsultationSpecialty
from tests.models import TestCategory

class Command(BaseCommand):
    help = 'Populate sample consultation specialties and test categories'

    def handle(self, *args, **options):
        # Create consultation specialties
        specialties = [
            {
                'name': 'Gynecology',
                'description': 'Women\'s health, reproductive health, pregnancy care, and gynecological conditions.',
                'price': 15000.00,
                'duration_minutes': 45
            },
            {
                'name': 'General Physician',
                'description': 'General medical consultation for common health issues, preventive care, and health screening.',
                'price': 10000.00,
                'duration_minutes': 30
            },
            {
                'name': 'Radiology',
                'description': 'Medical imaging consultation, X-ray, ultrasound, and CT scan interpretation.',
                'price': 20000.00,
                'duration_minutes': 30
            },
            {
                'name': 'Chemical Pathology',
                'description': 'Laboratory test interpretation, biochemical analysis, and metabolic disorders.',
                'price': 12000.00,
                'duration_minutes': 30
            },
            {
                'name': 'Microbiology',
                'description': 'Infectious disease consultation, antimicrobial therapy, and infection control.',
                'price': 12000.00,
                'duration_minutes': 30
            },
            {
                'name': 'Hematology',
                'description': 'Blood disorders, anemia, bleeding disorders, and blood cancer consultation.',
                'price': 15000.00,
                'duration_minutes': 40
            }
        ]

        for specialty_data in specialties:
            specialty, created = ConsultationSpecialty.objects.get_or_create(
                name=specialty_data['name'],
                defaults=specialty_data
            )
            if created:
                self.stdout.write(f'Created specialty: {specialty.name}')
            else:
                self.stdout.write(f'Specialty already exists: {specialty.name}')

        # Create test categories
        categories = [
            'General Health',
            'Sexual Health',
            'Cardiac Health',
            'Diabetes & Metabolism',
            'Liver Function',
            'Kidney Function',
            'Thyroid Function',
            'Infectious Diseases',
            'Cancer Screening',
            'Pregnancy & Fertility',
            'Allergy Testing',
            'Nutritional Assessment'
        ]

        for category_name in categories:
            category, created = TestCategory.objects.get_or_create(name=category_name)
            if created:
                self.stdout.write(f'Created category: {category.name}')
            else:
                self.stdout.write(f'Category already exists: {category.name}')

        self.stdout.write(self.style.SUCCESS('Successfully populated sample data!'))