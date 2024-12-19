from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Deletes a user by username'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = kwargs['username']
        try:
            user = User.objects.get(username=username)
            user.delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted user "{username}"'))
        except User.DoesNotExist:
            self.stdout.write(self.style.WARNING(f'User "{username}" does not exist')) 