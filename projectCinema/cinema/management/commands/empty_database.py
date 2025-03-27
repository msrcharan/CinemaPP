from django.core.management.base import BaseCommand
from cinema.models import Movie, Show, Screen  # Import your model

class Command(BaseCommand):
    help = 'Empties the movies table'

    def handle(self, *args, **options):
        Movie.objects.all().delete()
        Show.objects.all().delete()
        Screen.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all movies.'))