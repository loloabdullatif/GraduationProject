# Generated by Django 4.2.5 on 2023-12-06 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('graduationapp', '0003_remove_restaurant_menutype'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='restaurantId',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='graduationapp.restaurant'),
        ),
    ]
