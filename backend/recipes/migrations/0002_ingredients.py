import csv

from django.db import migrations


def add_ingredients(apps, schema_editor):
    Ingredient = apps.get_model('recipes', 'Ingredient')
    with open('data/ingredients.csv', encoding='utf-8') as ingredients:
        reader = csv.reader(ingredients)
        for row in reader:
            Ingredient.objects.create(name=row[0], measurement_unit=row[1])


def remove_ingredients(apps, schema_editor):
    Ingredient = apps.get_model('recipes', 'Ingredient')
    Ingredient.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_ingredients, remove_ingredients),
    ]
