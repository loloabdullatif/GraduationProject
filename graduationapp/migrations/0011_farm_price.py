# Generated by Django 4.2.4 on 2024-01-23 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graduationapp', '0010_tablebooking_userid'),
    ]

    operations = [
        migrations.AddField(
            model_name='farm',
            name='price',
            field=models.FloatField(default=0.0, max_length=10),
        ),
    ]
