# Generated by Django 4.2.5 on 2024-02-24 12:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('graduationapp', '0015_remove_farmbooking_price_remove_roombooking_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publicplace',
            name='rating',
        ),
    ]