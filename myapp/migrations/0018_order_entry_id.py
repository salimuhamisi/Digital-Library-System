# Generated by Django 5.0.3 on 2024-04-03 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0017_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='entry_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]