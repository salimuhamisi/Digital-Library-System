# Generated by Django 5.0.3 on 2024-03-23 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrowing',
            name='is_borrowed',
            field=models.BooleanField(default=False),
        ),
    ]