# Generated by Django 2.2.1 on 2019-06-11 15:12

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
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_driver', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
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
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plate', models.CharField(default='00a00000', max_length=8)),
                ('car_model', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_name', models.CharField(default=None, max_length=100)),
                ('price_per_km', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('price_per_layover_min', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(default=datetime.date(2019, 6, 11))),
                ('expire_date', models.DateField(default=datetime.date(2019, 6, 11))),
                ('percentage', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Prize',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('trip_count', models.IntegerField(default=999)),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('driver_score', models.IntegerField(default=None)),
                ('customer_score', models.IntegerField(blank=True, default=None, null=True)),
                ('comment_text', models.CharField(default=None, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Templatecomments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('wallet', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('customer_city', models.ForeignKey(on_delete=None, to='taxi.City')),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('wallet', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('enabled', models.BooleanField(default=False)),
                ('car', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='taxi.Car')),
                ('city', models.ForeignKey(on_delete=None, to='taxi.City')),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(default=datetime.datetime(2019, 6, 11, 19, 42, 16, 643970))),
                ('start_long_position', models.DecimalField(decimal_places=3, default=0, max_digits=8)),
                ('start_lat_position', models.DecimalField(decimal_places=3, default=0, max_digits=8)),
                ('destination_long_position', models.DecimalField(decimal_places=3, default=0, max_digits=8)),
                ('destination_lat_position', models.DecimalField(decimal_places=3, default=0, max_digits=8)),
                ('score', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='taxi.Score')),
                ('customer', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='taxi.Customer')),
                ('driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='taxi.Driver')),
            ],
        ),
        migrations.CreateModel(
            name='Moneytransfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('elec_cash', models.BooleanField(default=False)),
                ('amount', models.DecimalField(decimal_places=2, default=None, max_digits=6)),
                ('done', models.BooleanField(default=False)),
                ('trip', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='taxi.Trip')),
            ],
        ),
        migrations.CreateModel(
            name='Layover',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_minutes', models.IntegerField(default=0)),
                ('long_position', models.DecimalField(decimal_places=3, default=0, max_digits=8)),
                ('lat_position', models.DecimalField(decimal_places=3, default=0, max_digits=8)),
                ('trip', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='taxi.Trip')),
            ],
        ),
        migrations.CreateModel(
            name='Commonaddresses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('long_position', models.DecimalField(decimal_places=3, default=0, max_digits=8)),
                ('lat_position', models.DecimalField(decimal_places=3, default=0, max_digits=8)),
                ('customer', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='taxi.Customer')),
            ],
        ),
    ]