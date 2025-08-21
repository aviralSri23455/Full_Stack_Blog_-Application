from django.core.management.base import BaseCommand
from blogs.mongodb_service import mongodb_service


class Command(BaseCommand):
    help = 'Set all blogs to published status'

    def handle(self, *args, **options):
        try:
            # Update all blogs in MongoDB to be published
            if mongodb_service.db:
                result = mongodb_service.blogs_collection.update_many(
                    {},  # Update all blogs
                    {"$set": {"is_published": True}}
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully updated {result.modified_count} blogs to published status')
                )
            else:
                self.stdout.write(
                    self.style.ERROR('MongoDB connection not available')
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error: {str(e)}')
            )
