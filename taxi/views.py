from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as lg
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.views.decorators.csrf import csrf_exempt
from decimal import *


# Create your views here.
def home(request):
    driver_sign_up_form = driver_sign_up()
    driver_sign_in_form = driver_sign_in()
    customer_sign_in_form = customer_sign_in()
    customer_sign_up_form = customer_sign_up()
    context = {
        'message': '',
        'driver_sign_up_form': driver_sign_up_form,
        'driver_sign_in_form' : driver_sign_in_form,
        'customer_sign_in_form' : customer_sign_in_form,
        'customer_sign_up_form' : customer_sign_up_form
    }
    return render(request, 'index.html', context)


#todo fix sign up for customer


@login_required(login_url='')
def customer_dashboardview(request):
    cust = Customer.objects.get(user = request.user)
    print(request.user)
    no_trips = Trip.objects.filter(customer=cust).count()
    scores_avg = Score.objects.filter(trip__customer=cust).aggregate(Avg('customer_score'))['customer_score__avg']
    if scores_avg is None:
        scores_avg = 0
    comrad = Commonaddresses.objects.filter(customer = cust)


    #all done trips
    moneytransfers = Moneytransfer.objects.filter(trip__customer = cust, done = True).order_by('-trip__date_time')

    #discounts
    discount = None
    if Discount.objects.filter(customer=cust).exists():
        discount = Discount.objects.get(customer = cust)

    #prizes
    trip_no = moneytransfers.count()
    prizes = None
    if trip_no != request.user.last_prize:
        prizes = Prize.objects.filter(trip_count = trip_no)
        for p in prizes:
            cust.wallet += p.amount
            cust.save()
            request.user.last_prize = trip_no
            request.user.save()

    #pending trip
    pendingmoney = None
    if (Trip.objects.filter(customer=cust, driver = None)):
        pendingmoney = Moneytransfer.objects.get(trip__customer = cust, trip__driver=None)

    context = {"is_authenticated": request.user.is_authenticated, "customer": cust, 'no_trips': no_trips,
               'avg': scores_avg, "common_address" : comrad, "moneytransfers": moneytransfers,
               "discount": discount, "pendingmoney": pendingmoney, "prizeamount" : prizes }

    return render(request, 'customer_dash.html', context)

@login_required(login_url='')
def driver_dashboardview(request):

    driv = Driver.objects.get(user=request.user)

    no_trips = Trip.objects.filter(driver=driv).count()
    scores_avg = Score.objects.filter(trip__driver=driv).aggregate(Avg('driver_score'))['driver_score__avg']
    if scores_avg is None:
        scores_avg = 0

    # all done trips
    moneytransfers = Moneytransfer.objects.filter(trip__driver=driv).order_by('-trip__date_time')

    # pending trip
    pendingmoneys = Moneytransfer.objects.filter(trip__driver=None, trip__customer__customer_city= driv.city).order_by('-trip__date_time')

    # prizes
    trip_no = moneytransfers.count()
    prizes = None
    if trip_no != request.user.last_prize:
        prizes = Prize.objects.filter(trip_count=trip_no)
        for p in prizes:
            driv.wallet += p.amount
            driv.save()
            request.user.last_prize = trip_no
            request.user.save()


    context = {"is_authenticated": request.user.is_authenticated, "driver": driv, 'no_trips': no_trips,
               'avg': scores_avg, "moneytransfers": moneytransfers, "pendingmoneys": pendingmoneys, "prizeamount" : prizes }

    return render(request,'driver_dash.html', context)


def driver_sign_up_view(request):
    if request.method == 'POST':

        driver_sign_up_form = driver_sign_up(request.POST)

        if driver_sign_up_form.is_valid():
            data = driver_sign_up_form.cleaned_data

            driver_sign_in_form = driver_sign_in()
            customer_sign_in_form = customer_sign_in()
            customer_sign_up_form = customer_sign_up()

            if User.objects.filter(username=data['username']).exists():
                context = {
                    'message': 'a Driver with this username exists! Choose another one.',
                    'driver_sign_up_form': driver_sign_up_form,
                    'driver_sign_in_form': driver_sign_in_form,
                    'customer_sign_in_form': customer_sign_in_form,
                    'customer_sign_up_form': customer_sign_up_form
                }
                return render(request, 'index.html', context)
            else:
                cir = Car.objects.create(car_model = data['car_model'], plate = data['car_plate'])
                cit = City.objects.get(city_name=data['city'])
                u = User.objects.create_user(username = data['username'], email=data['email'], password=data['password'], first_name = data['first_name'], last_name = data['last_name'], is_driver = True)
                d = Driver.objects.create( user=u, car = cir, city = cit)
                context = {
                    'message': 'your Profile has been submitted and needs to be validated by the Administrator. Thanks for being patient.',
                    'driver_sign_up_form': driver_sign_up_form,
                    'driver_sign_in_form': driver_sign_in_form,
                    'customer_sign_in_form': customer_sign_in_form,
                    'customer_sign_up_form': customer_sign_up_form
                }
                return render(request, 'index.html', context)

    else:
        driver_sign_up_form = driver_sign_up()
        driver_sign_in_form = driver_sign_in()
        customer_sign_in_form = customer_sign_in()
        customer_sign_up_form = customer_sign_up()
        context = {
            'message': '',
            'driver_sign_up_form': driver_sign_up_form,
            'driver_sign_in_form': driver_sign_in_form,
            'customer_sign_in_form': customer_sign_in_form,
            'customer_sign_up_form': customer_sign_up_form
        }
        return render(request, 'index.html', context)

def logout_view(request):
    logout(request)
    return home(request)

def driver_sign_in_view(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        driver_sign_in_form = driver_sign_in(request.POST)

        # check whether it's valid:
        if driver_sign_in_form.is_valid():
            # process the data in form.cleaned_data as required
            data = driver_sign_in_form.cleaned_data
            username = data['username']
            password = data['password']
            user = authenticate(username =username, password=password)
            if user is not None and User.objects.get(username=username).is_driver:
                # A backend authenticated the credentials
                u = User.objects.get(username=username)
                driv = Driver.objects.get(user=u)

                if not driv.enabled:
                    driver_sign_up_form = driver_sign_in()
                    customer_sign_in_form = customer_sign_in()
                    customer_sign_up_form = customer_sign_up()
                    context = {
                        'message': 'Your account is not yet validated by the Administrator. Please try again later.',
                        'driver_sign_up_form': driver_sign_up_form,
                        'driver_sign_in_form': driver_sign_in_form,
                        'customer_sign_in_form': customer_sign_in_form,
                        'customer_sign_up_form': customer_sign_up_form
                    }
                    return render(request, 'index.html', context)

                lg(request, user)
                return driver_dashboardview(request)

            else:
                # No backend authenticated the credentials
                # redirect to a new URL:
                driver_sign_up_form = driver_sign_in()
                customer_sign_in_form = customer_sign_in()
                customer_sign_up_form = customer_sign_up()
                context = {
                    'message': 'Wrong username or password.',
                    'driver_sign_up_form': driver_sign_up_form,
                    'driver_sign_in_form': driver_sign_in_form,
                    'customer_sign_in_form': customer_sign_in_form,
                    'customer_sign_up_form': customer_sign_up_form
                }
                return render(request, 'index.html', context)

    # if a GET (or any other method) we'll create a blank form
    else:
        driver_sign_up_form = driver_sign_up()
        driver_sign_in_form = driver_sign_in()
        customer_sign_in_form = customer_sign_in()
        customer_sign_up_form = customer_sign_up()
        context = {
            'message': '',
            'driver_sign_up_form': driver_sign_up_form,
            'driver_sign_in_form': driver_sign_in_form,
            'customer_sign_in_form': customer_sign_in_form,
            'customer_sign_up_form': customer_sign_up_form
        }
        return render(request, 'index.html', context)

def customer_sign_up_view(request):
    if request.method == 'POST':

        customer_sign_up_form = customer_sign_up(request.POST)

        if customer_sign_up_form.is_valid():
            data = customer_sign_up_form.cleaned_data

            if User.objects.filter(username=data['username']).exists():

                customer_sign_in_form = customer_sign_in()
                driver_sign_in_form = driver_sign_in()
                driver_sign_up_form = driver_sign_up()
                context = {
                    'message': 'a user with this username exists! Choose another one.',
                    'driver_sign_up_form': driver_sign_up_form,
                    'driver_sign_in_form': driver_sign_in_form,
                    'customer_sign_in_form': customer_sign_in_form,
                    'customer_sign_up_form': customer_sign_up_form
                }
                return render(request, 'index.html', context)
            else:
                cit = City.objects.get(city_name=data['city'])
                u = User.objects.create_user(username=data['username'], email=data['email'], password=data['password'], first_name=data['first_name'], last_name=data['last_name'] )
                c = Customer.objects.create(user = u, customer_city=cit)
                lg(request, u)
                return customer_dashboardview(request)
    else:
        driver_sign_up_form = driver_sign_up()
        driver_sign_in_form = driver_sign_in()
        customer_sign_in_form = customer_sign_in()
        customer_sign_up_form = customer_sign_up()
        context = {
            'message': '',
            'driver_sign_up_form': driver_sign_up_form,
            'driver_sign_in_form': driver_sign_in_form,
            'customer_sign_in_form': customer_sign_in_form,
            'customer_sign_up_form': customer_sign_up_form
        }
        return render(request, 'index.html', context)

def customer_sign_in_view(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        customer_sign_in_form = customer_sign_in(request.POST)

        # check whether it's valid:
        if customer_sign_in_form.is_valid():
            # process the data in form.cleaned_data as required
            data = customer_sign_in_form.cleaned_data
            username = data['username']
            password = data['password']
            user = authenticate(username =username, password=password)
            if user is not None and not User.objects.get(username=username).is_driver:
                # A backend authenticated the credentials
                lg(request, user)
                return customer_dashboardview(request)
            else:
                # No backend authenticated the credentials
            # redirect to a new URL:
                driver_sign_up_form = driver_sign_in()
                driver_sign_in_form = driver_sign_in()
                customer_sign_up_form = customer_sign_up()
                context = {
                    'message': 'Wrong username or password.',
                    'driver_sign_up_form': driver_sign_up_form,
                    'driver_sign_in_form': driver_sign_in_form,
                    'customer_sign_in_form': customer_sign_in_form,
                    'customer_sign_up_form': customer_sign_up_form
                }
                return render(request, 'index.html', context)

    # if a GET (or any other method) we'll create a blank form
    else:
        driver_sign_up_form = driver_sign_up()
        driver_sign_in_form = driver_sign_in()
        customer_sign_in_form = customer_sign_in()
        customer_sign_up_form = customer_sign_up()
        context = {
            'message': '',
            'driver_sign_up_form': driver_sign_up_form,
            'driver_sign_in_form': driver_sign_in_form,
            'customer_sign_in_form': customer_sign_in_form,
            'customer_sign_up_form': customer_sign_up_form
        }
        return render(request, 'index.html', context)

@csrf_exempt
@login_required(login_url='')
def customer_editprofile_view(request):
    if request.method == 'POST':
        fname = request.POST['first']
        lname = request.POST['last']
        cid = request.POST['option']

        cust = Customer.objects.get(user = request.user)
        cust.user.first_name = fname
        cust.user.last_name = lname
        cust.customer_city = City.objects.get(id = cid)

        cust.save()
        cust.user.save()
        cust.customer_city.save()
        
        return customer_dashboardview(request)
    else:
        cust = Customer.objects.get(user = request.user)
        context = {
            'cities': City.objects.all(),
            'customer': cust
        }
        return render(request, 'customer_editprofile.html', context)

@csrf_exempt
@login_required(login_url='')
def customer_filinyowallet_view(request):
    amount = request.POST['amount']
    cust = Customer.objects.get(user = request.user)
    cust.wallet += Decimal(amount)
    cust.save()

    return customer_dashboardview(request)

@csrf_exempt
@login_required(login_url='')
def customer_addcommonaddress_view(request):
    long = request.POST['longitude']
    lat = request.POST['latitude']
    cust = Customer.objects.get(user = request.user)
    Commonaddresses.objects.create(customer = cust, long_position = long, lat_position = lat)

    return customer_dashboardview(request)

@csrf_exempt
@login_required(login_url='')
def customer_deletecommonaddress_view(request):
    addid = request.POST['commonadd']
    Commonaddresses.objects.filter(id = addid).delete()

    return customer_dashboardview(request)

@csrf_exempt
@login_required(login_url='')
def customer_newtrip_view(request):
    starting_lat = request.POST['start_latitude']
    starting_long = request.POST['start_longitude']
    destination_lat = request.POST['dest_latitude']
    destination_long = request.POST['dest_longitude']

    cust = Customer.objects.get(user = request.user)
    tri = Trip.objects.create(customer = cust, start_lat_position = starting_lat, start_long_position = starting_long, destination_long_position = destination_long, destination_lat_position = destination_lat)


    layover1 = request.POST['layover1']
    if layover1:
        lay1_lat = request.POST['lay_latitude1']
        lay1_long = request.POST['lay_longitude1']
        Layover.objects.create(long_position = lay1_long, lat_position = lay1_lat, time_minutes = layover1, trip = tri)

        layover2 = request.POST['layover2']
        if layover2:
            lay2_lat = request.POST['lay_latitude2']
            lay2_long = request.POST['lay_longitude2']
            Layover.objects.create(long_position=lay2_long, lat_position=lay2_lat, time_minutes=layover2, trip=tri)

            layover3 = request.POST['layover3']
            if layover3:
                lay3_lat = request.POST['lay_latitude3']
                lay3_long = request.POST['lay_longitude3']
                lay3_time = request.POST['layover3']
                Layover.objects.create(long_position=lay3_long, lat_position=lay3_lat, time_minutes=layover3, trip=tri)


    elec_cash = request.POST.get('elec_cash', False)
    if elec_cash == 'on':
        elec_cash = True

    money_transfer = Moneytransfer.objects.create(elec_cash = elec_cash, trip = tri, amount = 0)
    money_transfer.calculateamount()

    #discount
    discamount=0
    if Discount.objects.filter(customer = cust).exists():
        discount = Discount.objects.get(customer = cust)
        discamount = discount.percentage

    if float(money_transfer.amount) * (1-discamount)/100 > float(cust.wallet):
        money_transfer.elec_cash = 0
    money_transfer.save()

    return customer_dashboardview(request)


@csrf_exempt
@login_required(login_url='')
def customer_deletetrip_view(request):
    tid = request.POST['tripdelete']
    tri = Trip.objects.get(id = tid)
    Moneytransfer.objects.get(trip= tri)
    Trip.objects.get(id = tid).delete()

    return customer_dashboardview(request)

@csrf_exempt
@login_required(login_url='')
def customer_scoreyodriver_submit_view(request):
    num = request.POST['score_number']
    com = request.POST['score_comment']
    tripid = request.POST['trip_id']
    trip = Trip.objects.get(id = tripid)
    trip.score.driver_score = num
    trip.score.comment_text = com
    trip.score.save()
    trip.save()

    return customer_dashboardview(request)

@csrf_exempt
@login_required(login_url='')
def customer_scoreyodriver_click_view(request):
    trip_id = request.POST['trip_id']
    #template comments
    tc = Templatecomments.objects.all()
    context = {
        'trip_id': trip_id,
        'templatecomments': tc,
    }
    return render(request, 'customer_scoredriver.html', context)

@csrf_exempt
@login_required(login_url='')
def driver_editprofile_view(request):
    if request.method == 'POST':
        fname = request.POST['first']
        lname = request.POST['last']
        cid = request.POST['option']
        plate = request.POST['plate']
        model = request.POST['model']

        driv = Driver.objects.get(user=request.user)
        if not Car.objects.filter(plate = plate).exists() or driv.car.plate == plate:
            driv.car.plate = plate
            driv.car.car_model = model

        driv.user.first_name = fname
        driv.user.last_name = lname
        driv.city = City.objects.get(id=cid)

        driv.save()
        driv.user.save()
        driv.city.save()

        return driver_dashboardview(request)
    else:
        driv = Driver.objects.get(user=request.user)
        context = {
            'cities': City.objects.all(),
            'driver': driv
        }
        return render(request, 'driver_editprofile.html', context)


@csrf_exempt
@login_required(login_url='')
def driver_accepttrip_view(request):
    tripid = request.POST['chosentrip']
    trip = Trip.objects.get(id = tripid)
    driv = Driver.objects.get(user = request.user)
    trip.driver = driv

    #complete money transfer
    moneytransfer = Moneytransfer.objects.get(trip = trip)

    #electronic
    if moneytransfer.elec_cash == 1:

        # discount
        discamount = 0
        if Discount.objects.filter(customer=trip.customer).exists():
            discount = Discount.objects.get(customer=trip.customer)
            discamount = discount.percentage
            discount.delete()

        trip.customer.wallet = float(trip.customer.wallet) - float(moneytransfer.amount) * (1 - discamount) / 100
        trip.driver.wallet = trip.driver.wallet + moneytransfer.amount
        trip.customer.save()
        trip.driver.save()
    moneytransfer.done = True
    moneytransfer.save()

    newscore = Score.objects.create()
    trip.score = newscore

    trip.save()

    return render(request, 'driver_scorecustomer.html', context={'tripid' : tripid})


@csrf_exempt
@login_required(login_url='')
def driver_scoreyocustomer_view(request):
    tripid = request.POST['trip_id']
    num = request.POST['score_number']
    trip = Trip.objects.get(id = tripid)
    trip.score.customer_score = num
    trip.score.save()
    trip.save()

    return driver_dashboardview(request)

