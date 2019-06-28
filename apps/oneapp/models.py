from django.db import models
from datetime import datetime

class Admin(models.Model):
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Order(models.Model):
    date = models.DateField(default=datetime.now)
    total = models.DecimalField(max_digits = 5, decimal_places=2)
    status = models.CharField(max_length=255)
    sfirst_name = models.CharField(max_length=255)
    slast_name = models.CharField(max_length=255)
    saddress = models.CharField(max_length=255)
    saddress2 = models.CharField(max_length=255, default = "")
    scity = models.CharField(max_length=255)
    sstate = models.CharField(max_length=40)
    szipcode = models.CharField(max_length=55)
    bfirst_name = models.CharField(max_length=255, default = "")
    blast_name = models.CharField(max_length=255, default = "")
    baddress = models.CharField(max_length=255, default = "")
    baddress2 = models.CharField(max_length=255, default = "")
    bcity = models.CharField(max_length=255, default = "")
    bstate = models.CharField(max_length=40, default = "")
    bzipcode = models.CharField(max_length=55, default = "")
    card = models.CharField(max_length=55)
    security = models.CharField(max_length=55)
    expiration = models.CharField(max_length=55)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    #products_included = a list of products included in an order

class Sport(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    #products_list = a list of products that the sport has
    

class Product(models.Model):
    name = models.CharField(max_length=255)
    the_sport = models.ForeignKey(Sport,related_name="products_list")
    inventory = models.IntegerField(default=100)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    orders= models.ManyToManyField(Order, related_name="products_included") #a list of orders a product is in
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


    
