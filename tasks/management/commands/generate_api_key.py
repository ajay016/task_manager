from django.core.management.base import BaseCommand
from django.conf import settings
import secrets

class Command(BaseCommand):
    help = 'Generate a shared API key'

    def handle(self, *args, **options):
        shared_api_key = secrets.token_urlsafe(32)  # Generate a random API key
        settings.REST_FRAMEWORK_API_KEY = shared_api_key  # Set the key in settings
        self.stdout.write(self.style.SUCCESS(f'Shared API key: {shared_api_key}'))
