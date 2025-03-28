# Generated by Django 5.1.4 on 2025-01-02 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RandDealer', '0006_alter_cars_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='userconfirmation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('code', models.CharField(max_length=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
