from django.db import models
from django.utils import timezone
from datetime import date
import datetime
from datetime import datetime

# Create your models here.
class customer(models.Model):
    b_email = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    phno = models.CharField(max_length=10, null=True)
    dl_num = models.CharField(max_length=13, null=True)

    class Meta:
        db_table = "customer"


class address(models.Model):
    bid = models.ForeignKey('customer', on_delete=models.CASCADE, null=False)
    address = models.TextField()
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    pincode = models.IntegerField()

    class Meta:
        db_table = "address"        


class category(models.Model):
    name = models.CharField(max_length=30)
    luggage = models.CharField(max_length=10)
    num_people = models.CharField(max_length=10)
    cost = models.CharField(max_length=10) #per day
    late_fee = models.CharField(max_length=10) #per hour   

    class Meta:
        db_table = "Category"  


class car(models.Model):
    reg_number = models.CharField(max_length=15)        
    name = models.CharField(max_length=20)
    mileage = models.CharField(max_length=10)
    availability = models.IntegerField()
    category = models.ForeignKey('category',on_delete=models.SET_NULL,null=True)
    photo = models.ImageField(blank=True)

    class Meta:
        db_table ="car"

    def getabsoluteurl(self):
        return "/car_detail/%i/" % self.id
    


class booking(models.Model):
    
    from_date = models.DateTimeField(default=datetime.today)
    ret_date = models.DateTimeField(default=datetime.today)
    amt = models.IntegerField(null=True)
    status	= models.IntegerField(null=True)    #0 - not returned   1 - returned
    pickup_loc = models.ForeignKey('address', on_delete=models.SET_NULL,null=True,related_name='pickup')
    drop_loc = models.ForeignKey('address', on_delete=models.SET_NULL,null=True, related_name='drop')	
    reg_num = models.ForeignKey('car', on_delete=models.CASCADE,null=False)	
    dl_num = models.ForeignKey('customer', on_delete=models.CASCADE,null=False)	
    act_ret_date =  models.DateTimeField(blank=True, null=True)    

    class Meta:
        unique_together = ("reg_num", "dl_num")
        db_table ="booking"


class billing(models.Model):
    bill_date =  models.DateTimeField(blank=True, null=True) 	
    bill_status	= models.IntegerField(blank=True, null=True) #0 - not payed   1 - payed
    late_fee = models.IntegerField(blank=True, null=True)	
    tax_amount	= models.IntegerField(blank=True, null=True)	
    booking_id = models.ForeignKey('booking', on_delete=models.CASCADE,null=False)		
    total_amount = models.IntegerField(blank=True, null=True)	         

    class Meta:
        db_table ="billing"