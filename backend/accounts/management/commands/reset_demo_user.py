from django.core.management.base import BaseCommand
from accounts.models import CustomUser


class Command(BaseCommand):
    help = 'Reset demo user password'

    def handle(self, *args, **options):
        try:
            user = CustomUser.objects.get(email='demo@gmail.com')
            user.set_password('12345678')
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'Successfully updated password for user: {user.email}')
            )
        except CustomUser.DoesNotExist:
            # Create the user if it doesn't exist
            user = CustomUser.objects.create_user(
                email='demo@gmail.com',
                username='demo',
                password='12345678'
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created user: {user.email}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error: {str(e)}')
            )
