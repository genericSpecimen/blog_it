import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Create initial superuser if not exists"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "adminpass")

        if not User.objects.filter(username=username).exists():
            print("Creating superuser...")
            User.objects.create_superuser(username=username, email=email, password=password)
        else:
            print("Superuser already exists.")
