from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import Event
from datetime import timedelta

class Command(BaseCommand):
    help = 'Creates sample events for testing'

    def handle(self, *args, **kwargs):
        # Clear existing events
        Event.objects.all().delete()

        # Create sample events
        events = [
            {
                'title': 'Workshop de Integración',
                'title_en': 'Integration Workshop',
                'title_es': 'Workshop de Integración',
                'description': 'Aprende sobre la cultura local y comparte tus experiencias',
                'description_en': 'Learn about local culture and share your experiences',
                'description_es': 'Aprende sobre la cultura local y comparte tus experiencias',
                'date': timezone.now().replace(hour=15, minute=0),
                'location': 'Centro Comunitario',
                'online': False
            },
            {
                'title': 'Sesión de Yoga Online',
                'title_en': 'Online Yoga Session',
                'title_es': 'Sesión de Yoga Online',
                'description': 'Clase de yoga para todos los niveles',
                'description_en': 'Yoga class for all levels',
                'description_es': 'Clase de yoga para todos los niveles',
                'date': timezone.now() + timedelta(days=2),
                'location': 'Zoom',
                'online': True,
                'meeting_link': 'https://zoom.us/j/example'
            },
            {
                'title': 'Asesoría Legal Gratuita',
                'title_en': 'Free Legal Advice',
                'title_es': 'Asesoría Legal Gratuita',
                'description': 'Consultas sobre procesos migratorios',
                'description_en': 'Immigration process consultations',
                'description_es': 'Consultas sobre procesos migratorios',
                'date': timezone.now() + timedelta(days=5),
                'location': 'Oficina Central',
                'online': False
            }
        ]

        for event_data in events:
            Event.objects.create(**event_data)
            self.stdout.write(f"Created event: {event_data['title']}")

        self.stdout.write(self.style.SUCCESS('Successfully created sample events'))
