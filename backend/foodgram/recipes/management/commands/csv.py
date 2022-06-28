import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '-f', '--file',
            dest='filename',
            help='specify csv filename',
            metavar="FILE")

    def handle(self, *args, **options):
        Ingredient.objects.all().delete()
        data = options['filename'] or '../../data/ingredients.csv'
        with open(
            data, 'r', encoding='utf-8'
        ) as cg_csv:
            reader = csv.DictReader(cg_csv)
            for row in reader:
                ingredient = Ingredient(**row)
                ingredient.save()
        self.stdout.write(self.style.SUCCESS(
            'Successfully import ingredients')
        )
