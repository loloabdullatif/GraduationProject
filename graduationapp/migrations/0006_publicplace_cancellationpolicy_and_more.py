# Generated by Django 4.2.4 on 2023-12-10 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graduationapp', '0005_alter_touristauser_phonenumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicplace',
            name='cancellationPolicy',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='publicplace',
            name='facebookLink',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='publicplace',
            name='instagramLink',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='publicplace',
            name='kilometersFromCityCenter',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='publicplace',
            name='policies',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='table',
            name='capacity',
            field=models.IntegerField(default=4),
        ),
        migrations.AddField(
            model_name='table',
            name='tableType',
            field=models.CharField(choices=[('standard', 'Standard'), ('bar', 'Bar'), ('high_top', 'High Top')], default=1, max_length=20),
        ),
    ]
