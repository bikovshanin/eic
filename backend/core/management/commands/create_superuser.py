import os

import django
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a superuser if one does not already exist'

    def handle(self, *args, **options):

        username = os.getenv('DJANGO_SUPERUSER_USERNAME')
        email = os.getenv('DJANGO_SUPERUSER_EMAIL')
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f'Superuser {username} created.')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Superuser {username} already exists.')
            )
