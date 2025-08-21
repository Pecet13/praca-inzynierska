from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.services import user_path_exists
from api.models import Comparison


class Command(BaseCommand):
    help = 'Update product rankings based on user comparisons'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user_id',
            type=int,
            help='ID of the user to check for transitive comparisons (default value is 1)',
            default=1,
        )

    def handle(self, *args, **options):
        try:
            comparisons = Comparison.objects.filter(user=options['user_id'])
            username = User.objects.get(id=options['user_id']).username
            self.stdout.write(f'Checking transitive comparisons for user: {username}')
            non_transitive = []
            for comparison in comparisons:
                if comparison.result == 'More':
                    if user_path_exists(
                        options['user_id'],
                        comparison.category,
                        comparison.product2.id,
                        comparison.product1.id,
                    ):
                        non_transitive.append(comparison)
                elif comparison.result == 'Less':
                    if user_path_exists(
                        options['user_id'],
                        comparison.category,
                        comparison.product1.id,
                        comparison.product2.id,
                    ):
                        non_transitive.append(comparison)
            self.stdout.write(f'Checked {comparisons.count()} comparisons.')
            self.stdout.write(f'Non-transitive comparisons found: {len(non_transitive)}')
            percentage = (
                (len(non_transitive) / comparisons.count()) * 100
                if comparisons.count() > 0
                else 0
            )
            self.stdout.write(
                self.style.SUCCESS(f'Non-transitive percentage: {percentage:.2f}%')
            )
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error updating rankings: {e}'))
