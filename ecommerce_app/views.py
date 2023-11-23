from django.shortcuts import render,redirect
from .models import products,customer
from django.contrib.auth.hashers import make_password
from django.views import View
# Create your views here.

def home (request):
    products_to_post = products.get_all_products()
    return render(request,'home.html',{'products_to_post':products_to_post})

def detail_view(request,id):
    products_to_post = products.objects.get(id=id)
    return render(request,'view_details.html',{'products_to_post':products_to_post})


class Signup(View):
    def  get(self,request):
        return render(request,'sign_up.html')
    ##### function to coneect to formulario
    def post(self,request):
        postData= request.POST
        first_name = postData.get('')
        last_name = postData.get('')
        phone = postData.get('')
        email = postData.get('')
        password = postData.get('')
        
        ## validation
        value = {
            'first_name':first_name,
            'last_name':last_name,
            'phone':phone,
            'email':email
        }
        error_message = None
        
        # This information is for updating the information model
        customer = customer(first_name=first_name,
                            last_name = last_name,
                            phone=phone,
                            email=email,
                            password=password)
        
        error_message = self.validateCustomer(customer)
        if not error_message:
            print(first_name,last_name,phone,email,password)
            customer.password = make_password (customer.password)
            return redirect('home.html')
        else:
            data = {
                'error': error_message,
                'values': value
            }
        return (request,'signup.html',data)
    
    def validateCustomer(self,customer):
        error_message = None
        
        if not customer.first_name:
            error_message = 'Please Enter your First Name !!'
        elif len (customer.first_name) <3:
            error_message = 'First Name must be 3 char long or more'
        elif not customer.last_name:
            error_message = 'Please Enter your Last name !!'
        elif len(customer.last_name) <3:
            error_message = 'Last name must be 3 char long or more'
        elif not customer.phone:
            error_message = 'Enter your Phone Number'
        elif len(customer.phone) <3 :
            error_message = 'Your number phone must be 10 char long'
        elif len (customer.password) < 5:
            error_message = 'Password must be 5 char long'
        elif len (customer.email) < 5:
            error_message = 'Email must be 5 char long'
        elif customer.isExists ():
            error_message = 'Email Address Already Registered..'
        # saving

        return error_message