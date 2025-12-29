"""
Management command to create admin superuser.
"""
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Create admin superuser if it does not exist'

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'aifaadmin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@aifasports.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'AifaAdmin2024!')

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully'))
        else:
            user = User.objects.get(username=username)
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" password updated'))
