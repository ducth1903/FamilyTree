from django.core.management.base import BaseCommand
from tree.models import Couple

class Command(BaseCommand):
    help = 'Empty/Delete Couple model in database'
    def handle(self, *args, **options):
        Couple.objects.all().delete()