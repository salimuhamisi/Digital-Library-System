# Generated by Django 5.0.3 on 2024-03-27 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_alter_borrowing_is_borrowed'),
    ]

    operations = [
        migrations.CreateModel(
            name='supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=70)),
                ('book_tittle', models.CharField(max_length=50)),
                ('number_of_books', models.IntegerField()),
                ('delivery_date', models.DateField()),
                ('contact', models.CharField(max_length=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
