from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
import math
import decimal
# Create your models here.

class City(models.Model):
    city_name = models.CharField(max_length=100, default=None)
    price_per_km = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    price_per_layover_min = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    def __str__(self):
        return self.city_name


class User(AbstractUser):
    is_driver = models.BooleanField(default=False)
    last_prize = models.IntegerField(default=0)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    customer_city = models.ForeignKey(City, on_delete=None)
    wallet = models.DecimalField(max_digits=6, decimal_places=2, default = 0)
    def __str__(self):
        return "{}".format(self.user)

class Commonaddresses(models.Model):
    customer = models.ForeignKey(Customer, on_delete= models.CASCADE, default = None)
    long_position   = models.DecimalField (max_digits=8, decimal_places=3,  default=0)
    lat_position   = models.DecimalField (max_digits=8, decimal_places=3,  default=0)
    def __str__(self):
        return "{} {}".format(self.customer, self.id)


class Car(models.Model):
    plate = models.CharField(max_length=8, default = '00a00000', unique=True)
    car_model = models.CharField(max_length=100, default= '')
    def __str__(self):
        return self.plate


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    city = models.ForeignKey(City, on_delete=None)
    wallet = models.DecimalField(max_digits=6, decimal_places=2, default = 0)
    enabled =  models.BooleanField(default = False)
    car = models.OneToOneField(Car, on_delete=models.CASCADE, unique=True)
    def __str__(self):
        return "{}".format(self.user)


class Score(models.Model):
    driver_score = models.IntegerField( default = 0)
    customer_score = models.IntegerField(default = 0)
    comment_text = models.CharField(max_length=255, default = None, blank=True, null=True)

    def __str__(self):
        return "{}".format(self.id)


class Trip(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default= None)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, blank=True, null=True)
    score = models.OneToOneField(Score, on_delete=models.DO_NOTHING, blank=True, null=True)
    date_time = models.DateTimeField(default= datetime.datetime.now())
    start_long_position = models.DecimalField (max_digits=8, decimal_places=3,  default=0)
    start_lat_position = models.DecimalField (max_digits=8, decimal_places=3,  default=0)
    destination_long_position = models.DecimalField (max_digits=8, decimal_places=3,  default=0)
    destination_lat_position = models.DecimalField (max_digits=8, decimal_places=3,  default=0)
    def __str__(self):
        return "{}".format(self.id)



class Layover(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, default=None)
    time_minutes = models.IntegerField(default = 0)
    long_position = models.DecimalField (max_digits=8, decimal_places=3,  default=0)
    lat_position = models.DecimalField (max_digits=8, decimal_places=3,  default=0)
    def __str__(self):
        return "{} {}".format(self.id, self.trip)


#TODO   DELETE AFTER USAGE
class Discount(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True, default=None)
    start_date = models.DateField(default= datetime.date.today())
    expire_date = models.DateField(default= datetime.date.today())
    percentage = models.FloatField(default = 0)
    def __str__(self):
        return "{} {}".format(self.customer, self.percentage)




class Prize(models.Model):
    amount = models.DecimalField(max_digits=6, decimal_places=2, default = 0)
    trip_count = models.IntegerField(default = 999)
    def __str__(self):
        return "{} {}".format(self.amount, self.trip_count)

class Moneytransfer(models.Model):
    elec_cash = models.BooleanField(default = False)
    trip = models.OneToOneField(Trip, on_delete=models.CASCADE, default=None)
    amount = models.DecimalField(max_digits=6, decimal_places=2, default = None)
    done = models.BooleanField(default = False)
    def __str__(self):
        return "{} {} {}".format(self.trip, self.elec_cash, self.amount)

    def calculateamount(self):
        #calculate layovertime and total distance
        layovers = Layover.objects.filter(trip=self.trip)
        tot_layover_time = 0
        tot_dist = math.sqrt((float(self.trip.start_lat_position) - float(self.trip.destination_lat_position)) ** 2 + (float(self.trip.start_long_position) - float(self.trip.destination_long_position)) ** 2)
        prev_long = float(self.trip.destination_long_position)
        prev_lat = float(self.trip.destination_lat_position)
        for l in layovers:
            tot_layover_time += l.time_minutes
            tot_dist += math.sqrt((prev_long - float(l.long_position)) ** 2 + (prev_lat - float(l.lat_position)) ** 2)
            prev_long = float(l.long_position)
            prev_lat = float(l.lat_position)

        cit = self.trip.customer.customer_city
        amount_calculate = decimal.Decimal(float(cit.price_per_km) * tot_dist + float(cit.price_per_layover_min) * tot_layover_time)
        self.amount = amount_calculate

class Templatecomments(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return "{}".format(self.text)
