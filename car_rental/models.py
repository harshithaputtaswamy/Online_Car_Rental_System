from django.db import models
from PIL import Image
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django import forms
import random
import string
import uuid
from django.utils import timezone
from datetime import date
import datetime
from datetime import datetime

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField("Customer", on_delete=models.CASCADE)
    mobile = models.CharField(max_length = 13)
    area = models.ForeignKey(Area, on_delete=models.PROTECT)

    class Meta:
        db_table = "Customer"

class Orders(models.Model):
    user = models.ForeignKey("Customer", on_delete=models.PROTECT)
    car_dealer = models.ForeignKey(CarDealer, on_delete=models.PROTECT)
    rent = models.CharField(max_length=8)
    vehicle = models.ForeignKey(Vehicles, on_delete=models.PROTECT)
    days = models.CharField(max_length = 3)
    is_complete = models.BooleanField(default = False)

    class Meta:
        db_table = "Orders"

class Area(models.Model):
    pincode = models.CharField(max_length = 6,unique=True)
    city = models.CharField(max_length = 20)

    class Meta:
        db_table = "Area"

class CarDealer(models.Model):
    car_dealer = models.CharField(max_length = 20)
    mobile = models.CharField(max_length = 13)
    area = models.OneToOneField(Area, on_delete=models.PROTECT)
    wallet = models.IntegerField(default = 0)

    class Meta:
        db_table = "CarDealer"

class Vehicles(models.Model):
    car_name = models.CharField(max_length = 20)
    color = models.CharField(max_length = 10)
    dealer = models.ForeignKey("CarDealer", on_delete = models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null = True)
    capacity = models.CharField(max_length = 2)
    is_available = models.BooleanField(default = True)
    description = models.CharField(max_length = 100)    

    class Meta:
        db_table = "Vehicles"

