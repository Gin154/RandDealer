# Generated by Django 5.1.4 on 2025-05-05 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RandDealer', '0015_alter_cars_mileage'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsletterSub',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]
