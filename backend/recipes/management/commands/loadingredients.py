import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

from ...models import Ingredient

class Command(BaseCommand):
    help = 'Загрузка ингредиентов json'

    def handle(self, *args, **options):
        file_path = os.path.join(settings.BASE_DIR, 'data', 'ingredients.json')

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for ingredient in data:
                    try:
                        Ingredient.objects.create(
                            name=ingredient["name"],
                            measurement_unit=ingredient["measurement_unit"]
                        )
                    except IntegrityError:
                        print(f'Ингредиент {ingredient["name"]} '
                              f'{ingredient["measurement_unit"]} '
                              f'уже есть в базе')

        except FileNotFoundError:
            raise CommandError('Файл отсутствует')
