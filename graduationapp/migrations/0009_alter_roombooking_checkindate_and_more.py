# Generated by Django 4.2.4 on 2023-12-16 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graduationapp', '0008_alter_roombooking_roomid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roombooking',
            name='checkInDate',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='roombooking',
            name='checkoutDate',
            field=models.DateField(),
        ),
    ]
