# Generated by Django 5.0.3 on 2024-03-19 19:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_books'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Books',
            new_name='Book',
        ),
    ]
