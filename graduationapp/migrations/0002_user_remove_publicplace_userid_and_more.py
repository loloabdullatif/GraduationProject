# Generated by Django 4.2.5 on 2023-10-04 09:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('graduationapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userName', models.CharField(default='', max_length=255, unique=True)),
                ('phoneNumber', models.CharField(default='', max_length=10)),
                ('password', models.CharField(default='', max_length=10)),
                ('nationalNumber', models.CharField(default='', max_length=15, unique=True)),
                ('birthDate', models.DateField()),
                ('isOwner', models.BooleanField()),
            ],
        ),
        migrations.RemoveField(
            model_name='publicplace',
            name='userId',
        ),
        migrations.AlterField(
            model_name='farmbooking',
            name='userId',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='graduationapp.user'),
        ),
        migrations.AlterField(
            model_name='roombooking',
            name='userId',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='graduationapp.user'),
        ),
    ]
