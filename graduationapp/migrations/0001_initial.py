# Generated by Django 4.2.5 on 2023-11-14 12:59

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='TouristaUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('nationalNumber', models.CharField(default='', max_length=15, unique=True)),
                ('birthDate', models.DateField()),
                ('phoneNumber', models.CharField(max_length=10)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Amenities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('hotel', 'Hotel'), ('restaurant', 'Restaurant'), ('farm', 'Farm')], max_length=20)),
                ('name', models.CharField(default='', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Cuisine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cuisine', models.CharField(choices=[('Tasting Menu', 'Tasting Menu'), ('Buffet Menu', 'Buffet Menu'), ('Specials Menu', 'Specials Menu'), ('Beverage Menu', 'Beverage Menu'), ('Kids Menu', 'Kids Menu')], max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Governate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='PublicPlace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isApproved', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('hotel', 'Hotel'), ('restaurant', 'Restaurant'), ('farm', 'Farm')], max_length=20)),
                ('phoneNumber', models.CharField(default='', max_length=10)),
                ('rating', models.IntegerField(default=1)),
                ('area', models.FloatField(default='', max_length=20)),
            ],
            options={
                'verbose_name_plural': 'public places',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roomType', models.CharField(choices=[('single', 'single'), ('double', 'double'), ('vipRoom', 'vipRoom'), ('studio', 'studio')], default=None, max_length=10)),
                ('price', models.FloatField(default='', max_length=10)),
                ('roomNumber', models.IntegerField(default=1)),
                ('bedType', models.CharField(choices=[('single', 'single'), ('double', 'double')], max_length=10)),
                ('area', models.FloatField(default='', max_length=20)),
                ('numberOfPeople', models.IntegerField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tableNumber', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='TableBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default='', max_length=20)),
                ('checkInTime', models.DateTimeField(blank=True, null=True)),
                ('checkoutTime', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TouristDestination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('latitude', models.DecimalField(decimal_places=6, default=0.0, max_digits=9, max_length=15)),
                ('longitude', models.DecimalField(decimal_places=6, default=0.0, max_digits=9, max_length=15)),
                ('description', models.CharField(max_length=3000)),
                ('cityId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='graduationapp.city')),
            ],
            options={
                'verbose_name_plural': 'Tourist Destinations',
            },
        ),
        migrations.CreateModel(
            name='Farm',
            fields=[
                ('publicplace_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='graduationapp.publicplace')),
                ('rentType', models.CharField(choices=[('daily', 'Daily'), ('monthly', 'Monthly')], max_length=30)),
            ],
            options={
                'verbose_name_plural': 'farms',
            },
            bases=('graduationapp.publicplace',),
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('publicplace_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='graduationapp.publicplace')),
                ('numberOfRooms', models.IntegerField(default=1)),
                ('numberOfStars', models.IntegerField(default=1)),
            ],
            options={
                'verbose_name_plural': 'hotels',
            },
            bases=('graduationapp.publicplace',),
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('publicplace_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='graduationapp.publicplace')),
                ('openTime', models.TimeField()),
                ('menuType', models.CharField(default='', max_length=500)),
            ],
            options={
                'verbose_name_plural': 'restaurants',
            },
            bases=('graduationapp.publicplace',),
        ),
        migrations.CreateModel(
            name='TouristDestinationImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.ImageField(blank=True, upload_to='DestinationImages/')),
                ('publicPlaceId', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='graduationapp.touristdestination')),
            ],
        ),
        migrations.CreateModel(
            name='Street',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=30)),
                ('cityId', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='graduationapp.city')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amenityId', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='graduationapp.amenities')),
                ('publicPlaceId', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='graduationapp.publicplace')),
            ],
        ),
        migrations.CreateModel(
            name='RoomBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default='', max_length=20)),
                ('checkInDate', models.DateField(default=datetime.date.today)),
                ('checkoutDate', models.DateField(default=datetime.date.today)),
                ('roomId', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='roomId', to='graduationapp.room')),
                ('userId', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='publicplace',
            name='streetId',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='graduationapp.street'),
        ),
        migrations.AddField(
            model_name='publicplace',
            name='userId',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.ImageField(blank=True, upload_to='images/')),
                ('publicPlaceId', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='graduationapp.publicplace')),
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='governateId',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='graduationapp.governate'),
        ),
        migrations.AddField(
            model_name='room',
            name='hotelId',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='graduationapp.hotel'),
        ),
        migrations.CreateModel(
            name='RestaurantCuisine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cuisineId', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='graduationapp.cuisine')),
                ('restaurantId', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='graduationapp.restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='FarmBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default='', max_length=20)),
                ('checkInDate', models.DateField(default=datetime.date.today)),
                ('checkoutDate', models.DateField(default=datetime.date.today)),
                ('userId', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('farmId', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='graduationapp.farm')),
            ],
        ),
    ]
