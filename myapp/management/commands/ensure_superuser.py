from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = "Ensure a superuser exists; create one if missing"

    def add_arguments(self, parser):
        parser.add_argument('--username', default=os.environ.get('DJANGO_SU_USERNAME', 'admin'))
        parser.add_argument('--password', default=os.environ.get('DJANGO_SU_PASSWORD', 'Admin123!ChangeMe'))
        parser.add_argument('--email', default=os.environ.get('DJANGO_SU_EMAIL', ''))

    def handle(self, *args, **opts):
        User = get_user_model()
        username = opts['username']
        email = opts['email']
        password = opts['password']
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' already exists"))
            return
        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created"))
