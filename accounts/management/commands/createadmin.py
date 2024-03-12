from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates an admin user if it does not exist'

    def handle(self, *args, **options):
        if not User.objects.filter(username='bigBlackAdmin').exists():
            User.objects.create_superuser('bigBlackAdmin', 'bigBlackAdmin@black.com', 'deezNutAreBigAndBlackToo99')
            self.stdout.write(self.style.SUCCESS('Successfully created a new admin user'))
        else:
            self.stdout.write('Admin user already exists.')
