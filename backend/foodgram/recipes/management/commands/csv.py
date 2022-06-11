import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):

    def handle(self, *args, **options):
        Ingredient.objects.all().delete()
        with open(
            '../../data/ingredients.csv', 'r', encoding='utf-8'
        ) as cg_csv:
            reader = csv.DictReader(cg_csv)
            for row in reader:
                ingredient = Ingredient(**row)
                ingredient.save()
        self.stdout.write(self.style.SUCCESS(
            'Successfully import ingredients')
        )
