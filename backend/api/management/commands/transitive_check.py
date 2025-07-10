from django.core.management.base import BaseCommand
from api.services import user_path_exists
from api.models import Comparison


class Command(BaseCommand):
    help = 'Update product rankings based on user comparisons'

    def handle(self, *args, **options):
        try:
            comparisons = Comparison.objects.filter(user=2)
            not_transitive = []
            for comparison in comparisons:
                if comparison.result == 'More':
                    if user_path_exists(2, comparison.category, comparison.product2.id, comparison.product1.id):
                        not_transitive.append(comparison)
                elif comparison.result == 'Less':
                    if user_path_exists(2, comparison.category, comparison.product1.id, comparison.product2.id):
                        not_transitive.append(comparison)
            print(f'Checked {comparisons.count()} comparisons.')
            print(f'Not transitive comparisons found: {len(not_transitive)}')
            print(not_transitive)
            percentage = (len(not_transitive) / comparisons.count()) * 100 if comparisons.count() > 0 else 0
            self.stdout.write(self.style.SUCCESS(f'Not transitive percentage: {percentage:.2f}%'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error updating rankings: {e}'))
