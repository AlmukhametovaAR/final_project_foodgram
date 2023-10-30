import csv

from django.db import migrations


def add_tags(apps, schema_editor):
    Tag = apps.get_model('recipes', 'Tag')
    with open('data/tags.csv', encoding='utf-8') as tags:
        reader = csv.reader(tags)
        for row in reader:
            Tag.objects.create(name=row[0], color=row[1], slug=row[0])


def remove_tags(apps, schema_editor):
    Tag = apps.get_model('recipes', 'Tag')
    Tag.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_ingredients'),
    ]

    operations = [
        migrations.RunPython(add_tags, remove_tags),
    ]
