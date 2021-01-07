from django.shortcuts import render
from django.utils.encoding import force_text
from .models import *
from datetime import date
import requests
from django.shortcuts import redirect
from django.db import connection
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, time, timedelta
import pytz

utc=pytz.UTC

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        user_email = request.user.email
        query = "select * from customer where b_email='"+user_email+"';"
        user = len(list(customer.objects.raw(query)))
        cursor = connection.cursor()
        if(user == 0):
            cursor.execute("insert into customer values('" +
                           user_email+"','"+request.user.username+"','null','null')")
    return render(request, 'home.html')


def car_list(request):
    cars = car.objects.all()
    if request.user.is_authenticated:
        user_email = request.user.email
        query = "select * from customer where b_email='"+user_email+"';"
        user = len(list(customer.objects.raw(query)))
        cursor = connection.cursor()
        if(user == 0):
            cursor.execute("insert into customer values('" +
                           user_email+"','"+request.user.username+"','null','null')")
    context = {
            'cars': cars,
            }
    return render(request, 'car_list.html',context)        


def car_detail(request,id):
    car_now = list(car.objects.filter(id=id))
    cat = category.objects.all()
    if request.user.is_authenticated:
        user_email = request.user.email
        cursor = connection.cursor()
        query = "select * from customer where b_email='"+user_email+"';"
        user = len(list(customer.objects.raw(query)))
        cursor = connection.cursor()
        if(user == 0):
            cursor.execute("insert into customer values('" +
                           user_email+"','"+request.user.username+"','null','null')")
        
        user_address = address.objects.filter(bid=request.user.email)
        addr_len = len(list(address.objects.filter(bid=request.user.email)))
    
        context = {
        "car": car_now[0],
        "id": id,
        "category": cat,
        'user_address': user_address,
            'addr_len': addr_len,
        }                   
        return render(request, 'car_detail.html',context)
    else:
        return HttpResponseRedirect('/oauth/login/google-oauth2/?next=/car_detail/'+id+'/')        
                           

def book_car(request):
    if request.user.is_authenticated:
        user = customer.objects.get(b_email=request.user.email)
        car_now = car.objects.get(id=request.POST['car_id'])
        print(car_now)
        car_now.category = category.objects.get(id=request.POST['cat_choice'])
        car_now.save()
        query = "select * from booking where dl_num_id='"+request.user.email+"' and reg_num_id="+request.POST['car_id']
        bid = customer.objects.get(b_email=request.user.email)
        cursor = connection.cursor()

        #create booking
        bookings = booking(
            reg_num=car.objects.get(id=request.POST['car_id']),
            dl_num=customer.objects.get(b_email=request.user.email),
            )

        bookings.save()

    response = redirect('/add_address_form/')
    return response    


def add_address_form(request):
    if request.user.is_authenticated:
        return render(request, 'address.html')


def add_address(request):
    if request.user.is_authenticated:
        user_email = request.user.email
        # print(request.POST)
        user = customer(
            name = request.POST['name'],
            phno = request.POST['phone'],
            dl_num = request.POST['dl_num'],
        )
        user.save()
        address1 = address(
            bid=customer.objects.get(b_email=user_email),
            address=request.POST['pick_address'],
            city=request.POST['pick_city'],
            state=request.POST['pick_state'],
            pincode=request.POST['pick_pincode']
        )
        address1.save()

        address2 = address(
            bid=customer.objects.get(b_email=user_email),
            address=request.POST['drop_address'],
            city=request.POST['drop_city'],
            state=request.POST['drop_state'],
            pincode=request.POST['drop_pincode']
        )
        address2.save()

        bookings = booking.objects.filter(dl_num=customer.objects.get(b_email = request.user.email))
        if bookings.exists():
            bookings = bookings.last()
        print("booking id ",bookings)
        car = bookings.reg_num
        cost_day = car.category.cost
        from_date = request.POST['pick_date']
        to_date = request.POST['drop_date']
        days = request.POST['numdays']
        tot_cost = int(cost_day)*int(days) 
        print("cost ",tot_cost)
        bookings.pickup_loc = address.objects.filter(address=request.POST['pick_address'])[0]
        bookings.drop_loc=address.objects.filter(address=request.POST['drop_address'])[0]
        bookings.amt = tot_cost
        bookings.from_date = from_date
        bookings.to_date = to_date
        bookings.status = 0
        bookings.confirm = 1
        bookings.save()

        return redirect('/booking_details/')    


def booking_details(request):
    if request.user.is_authenticated:
        booking_list = list(booking.objects.filter(dl_num=customer.objects.get(b_email = request.user.email),confirm=1))
        booking_list.reverse()
        print(booking_list, " bookings")    
        context = {'booking': booking_list}
        return render(request, 'booking_details.html',context)
    else:
        return HttpResponseRedirect('/oauth/login/google-oauth2/?next=/booking_details/')       


def billings(request):
    if request.user.is_authenticated:
        booking_detail = list(booking.objects.filter(dl_num=customer.objects.get(b_email = request.user.email)))
        
        print(booking_detail)
        billing_list = []
        for booking_details in booking_detail:
            print(booking_details.id)
            if booking_details.status == 1 and len(billing.objects.filter(booking_id=booking_details.id)) != 0:
                # booking_details.act_ret_date = datetime.today()
                # booking_details.save()
                days = str(booking_details.act_ret_date - booking_details.ret_date)
                print(days)
                # days = 3
                days = int(days.split(' ')[0])
                print(days)
                late_fee = int(booking_details.reg_num.category.late_fee)*days
                tax_amount = (int(booking_details.amt) + late_fee)*.03
                
                print(late_fee, tax_amount)
                # print()
                
                billing_details = billing.objects.get(booking_id=booking_details.id)
                billing_details.bill_date = utc.localize(datetime.today())
                billing_details.late_fee = late_fee
                billing_details.tax_amount = tax_amount
                billing_details.total_amount = int(booking_details.amt) + late_fee + tax_amount                   
                billing_details.bill_status = 1
                billing_details.save()
                
                car_booked = booking.objects.get(id=booking_details.id).reg_num                
                car_booked.availability = 1
                car_booked.save()
                billing_list.append(billing_details)
                
            else:
                if len(billing.objects.filter(booking_id=booking_details.id)) == 0:
                    billing_details = billing(     
                        bill_date = utc.localize(datetime.today()),
                        bill_status = 0,
                        late_fee = 0,
                        tax_amount = int(booking_details.amt)*.3,
                        total_amount = int(booking_details.amt) + 0 + 0,    
                        booking_id = booking_details
                        
                    )
                    billing_details.save()

            billing_list.reverse()
            context = {'billing': billing_list}    

        return render(request, 'billing.html', context)
    else:
        return HttpResponseRedirect('/oauth/login/google-oauth2/?next=/billings/')       
    