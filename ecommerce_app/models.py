from django.db import models
import datetime
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import make_password

# Create your models here.

class category(models.Model):
    name = models.CharField(max_length=50)
    
    @staticmethod
    def get_all_categories():
        return category.objects.all()
    
    def __str__(self):
        return self.name

class products(models.Model):
    name = models.CharField(max_length=60)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(category,on_delete=models.CASCADE,default=1)
    description = models.CharField(max_length=250,default='',blank=True,null=True)
    image = models.CharField(max_length=350)
    image_2 = models.CharField(max_length=350)
    image_3 = models.CharField(max_length=350)
    image_4 = models.CharField(max_length=350)
    image_5 = models.CharField(max_length=350)

    
    @staticmethod
    def get_products_by_id(ids):
        return products.objects.filter(id__in=ids)
    
    @staticmethod
    def get_all_products():
        return products.objects.all()

############################YOUR CURRENTLY CODE##############################
class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField (max_length=50)
    phone = models.CharField(max_length=10)
    email=models.EmailField()
    password = models.CharField(max_length=200)
    
   
    def register(self):
       self.save()


    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email = email)
        except:
            return None
        
    def isExists(self):
        if Customer.objects.filter(email = self.email):
            return True

        return False


class order(models.Model):
    product = models.ForeignKey(products,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    calle = models.CharField(max_length=50)
    num_interior = models.CharField(max_length=10)
    code_postal = models.CharField (max_length=10)
    address = models.CharField (max_length=50, default='', blank=True)
    phone = models.CharField (max_length=50, default='', blank=True)
    date = models.DateField (default=datetime.datetime.today)
    status = models.BooleanField (default=False)
    
    

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return order.objects.filter(customer=customer_id).order_by('-date')
