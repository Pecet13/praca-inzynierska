from django.core.management.base import BaseCommand
from api.services import update_rankings


class Command(BaseCommand):
    help = 'Update product rankings based on user comparisons'

    def handle(self, *args, **options):
        try:
            update_rankings()
            self.stdout.write(self.style.SUCCESS('Rankings updated successfully.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error updating rankings: {e}'))
