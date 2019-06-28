from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import *
import bcrypt
import re
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


def products(request):
    product_list = Product.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(product_list, 15)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {
        "all_sports" : Sport.objects.exclude(Q(id=1) | Q(id=2) | Q(id=3)),
        "first_three" : Sport.objects.all()[:3],
        "all_products" : Product.objects.all(),
        "products":products
    }

    return render(request, 'oneapp/browse_products.html', context)

def see_more(request):

    return redirect('/products')

def logandreg(request):
    return render(request, "oneapp/admin.html")

def register(request):
    errors = False
    if not EMAIL_REGEX.match(request.POST['email']):
        messages.error(request, 'Email is invalid')
        errors = True
    if(len(request.POST['password']) < 1):
        messages.error(request, 'Password is required')
        errors = True
    if(request.POST['password'] != request.POST['confirm_password']):
        messages.error(request, 'Passwords do not match')
        errors = True

    if(errors):
        return redirect('/')

    hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    admin = Admin.objects.create(
        email = request.POST['email'], 
        password = hashed, 
    )

    request.session['admin_id'] = admin.id
    return redirect('/order_dash')

def login(request):
    try:
        admin = Admin.objects.get(email = request.POST['email'])
        if(bcrypt.checkpw(request.POST['password'].encode(), admin.password.encode())):
            request.session['admin_id'] = admin.id
            return redirect('/order_dash')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('/')
    except Admin.DoesNotExist:
        messages.error(request, 'Invalid Credentials')
        return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def order_dash(request):
    if 'admin_id' not in request.session:
        messages.error(request, 'please log in or register')
        return redirect('/')
    else:
        context = {
            'all_orders' : Order.objects.all()
        }
        return render(request, 'oneapp/order_dash.html', context)

def orderpage(request, order_id):
    if 'admin_id' not in request.session:
        messages.error(request, 'please log in or register')
        return redirect('/')
    else:
        this_order = Order.objects.get(id = order_id )
        context = {
            'all_products' : this_order
        }
        return render(request, "oneapp/order_info.html", context)

def adminproducts(request):
    if 'admin_id' not in request.session:
        messages.error(request, 'please log in or register')
        return redirect('/')
    else:
        context = {
            'all_products' : Product.objects.all()
        }
        return render(request, 'oneapp/admin_products.html', context)

def editproducts(request, prod_id):
    return redirect('/')

def updatestat(request, order_id):
    this_order= Order.objects.get(id=order_id)
    this_order.status = request.POST['select_status']
    this_order.save()
    return redirect('/order_dash')

def carts(request):
    
    return render(request, 'oneapp/carts.html')

def createorder(request):
    Order.objects.create(
        total = 100,
        status = "shipped",
        sfirst_name = request.POST['fname'],
        slast_name = request.POST['lname'],
        saddress = request.POST['address'],
        saddress2 = request.POST['address2'],
        scity = request.POST['city'],
        sstate =request.POST['state'],
        szipcode =request.POST['zip'],
        bfirst_name = request.POST['fname_bill'],
        blast_name = request.POST['lname_bill'],
        baddress = request.POST['address_bill'],
        baddress2 = request.POST['address2_bill'],
        bcity = request.POST['city_bill'],
        bstate =request.POST['state_bill'],
        bzipcode =request.POST['zip_bill'],
        card =request.POST['card'],
        security =request.POST['security'],
        expiration =request.POST['expdate'],
    )
    return redirect ('/carts')

def show(request, product_id):
    
    return render (request, 'product_info.html')
    
