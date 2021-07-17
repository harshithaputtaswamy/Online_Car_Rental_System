from django.db import models
from django.utils import timezone
from datetime import date
import datetime
from datetime import datetime

# Create your models here.
class customer(models.Model):
    b_email = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    phno = models.CharField(max_length=50, null=True)
    dl_num = models.CharField(max_length=16, null=True)

    class Meta:
        db_table = "customer"

    def __str__(self):
        return self.b_email 

class address(models.Model):
    bid = models.ForeignKey('customer', on_delete=models.CASCADE)
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

    def __str__(self):
        return self.name    


class car(models.Model):
    reg_number = models.CharField(max_length=15)        
    name = models.CharField(max_length=20)
    mileage = models.CharField(max_length=10)
    availability = models.IntegerField() # 0 not available      1 available
    category = models.ForeignKey('category',on_delete=models.SET_NULL,null=True)
    photo = models.ImageField(blank=True)

    class Meta:
        db_table ="car"

    def getabsoluteurl(self):
        return "/car_detail/%i/" % self.id
    
    # def __str__(self):
    #     return self.name


class booking(models.Model):
    
    from_date = models.DateTimeField(default=datetime.today)
    ret_date = models.DateTimeField(default=datetime.today)
    amt = models.IntegerField(default=0)
    status	= models.IntegerField(null=True)    #0 - not returned   1 - returned
    pickup_loc = models.ForeignKey('address', on_delete=models.SET_NULL,null=True,related_name='pickup')
    drop_loc = models.ForeignKey('address', on_delete=models.SET_NULL,null=True, related_name='drop')	
    reg_num = models.ForeignKey('car', on_delete=models.SET_NULL,null=True)	
    dl_num = models.ForeignKey('customer', on_delete=models.CASCADE)	
    act_ret_date =  models.DateTimeField(blank=True, null=True)  
    confirm = models.IntegerField(default=0)  # 0 - not confirmed   1 - confirmed

    class Meta:
        unique_together = ("reg_num", "dl_num","from_date")
        db_table ="booking"

    def __str__(self):
        return self.dl_num.b_email + ' , ' + self.reg_num.name


class billing(models.Model):
    bill_date =  models.DateTimeField(blank=True, null=True) 	
    bill_status	= models.IntegerField(blank=True, null=True) #0 - not payed   1 - payed
    late_fee = models.IntegerField(blank=True, null=True)	
    tax_amount	= models.IntegerField(blank=True, null=True)	
    booking_id = models.ForeignKey('booking', on_delete=models.CASCADE,null=False)		
    total_amount = models.IntegerField(blank=True, null=True)	         

    class Meta:
        db_table ="billing"

    def __str__(self):
        return self.booking_id.dl_num.b_email + ' , ' + self.booking_id.reg_num.name 