# Generated by Django 5.0.3 on 2024-03-28 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_book_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='document',
            field=models.FileField(blank=True, null=True, upload_to='files/'),
        ),
    ]
