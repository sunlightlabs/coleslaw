
from django.core.management.base import BaseCommand

from laws.models import Law

class Command(BaseCommand):
    help = """Import the US legal code from Cornel's XML format."""

    def handle(self, **options):
        dirname = options['dirname']
