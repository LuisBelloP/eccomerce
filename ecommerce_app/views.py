from django.shortcuts import render,redirect,HttpResponseRedirect,get_object_or_404,HttpResponse
from .models import products,Customer,order
from django.contrib.auth.hashers import check_password,make_password
from django.views import View
from django.urls import reverse 

from googlemaps import Client as GoogleMaps
from django.conf import settings
from django.http import JsonResponse
import requests 
# Create your views here.


class Index(View):
    def post(self,request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]  = quantity-1
                else:
                    cart[product]  = quantity+1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        total_items = sum(cart.values())
        request.session['total_items'] = total_items  
        return redirect('home')
    
    def get(self,request):
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')

def store (request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products_to_post = products.get_all_products()
    print('you are : ', request.session.get('email'))
    return render(request,'index.html',{'products_to_post':products_to_post})

class Detail_view(View):
    
     def get(self,request,id):
        products_to_post = products.objects.get(id=id)
        return render(request,'view_details.html',{'products_to_post':products_to_post})



def aboutus(request):
    return render(request,'about_us.html')

class Signup(View):
    def  get(self,request):
        return render(request,'sign_up.html')
   
    ##### function to coneect to formulario
    def post(self,request):
        postData= request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone_number')
        email = postData.get('email')
        password = postData.get('password')
        
        ## validation
        value = {
            'first_name':first_name,
            'last_name':last_name,
            'phone':phone,
            'email':email
        }
        error_message = None
        
        # This information is for updating the information model
        customer = Customer(first_name=first_name,
                            last_name = last_name,
                            phone=phone,
                            email=email,
                            password=password
                            )
        
        error_message = self.validateCustomer(customer)
        if not error_message:
            print(first_name,last_name,phone,email,password)
            
            customer.password = make_password (customer.password)
            customer.register ()            
            return redirect('home')
        else:
            data = {
                'error': error_message,
                'values': value
            }
        return (request,'signup.html',data)
    
    def validateCustomer(self, customer):
        error_message = None
        if (not customer.first_name):
            error_message = "Please Enter your First Name !!"
        elif not customer.last_name:
            error_message = 'Please Enter your Last Name'
        elif not customer.phone:
            error_message = 'Enter your Phone Number'
        # saving

        return error_message
    


class Login(View):
    return_url = None
    
    def get(self,request):
      Login.return_url = request.GET.get('return_url')
      return render (request,'login.html')  
    
    def post(self,request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer :
            flag = check_password(password, customer.password)
            if flag:
                error_message = 'Validado'
                request.session['customer'] = customer.id
                request.session['email'] = customer.email
                if Login.return_url:
                    return HttpResponseRedirect (Login.return_url)
                ## correctly working
                else:
                    print(f'{customer.id}')
                    print(f'{customer.email}')
                    Login.return_url = None
                    return redirect ('home')
                
            else:
                error_message = 'Contraseña o Email incorrecto!!'
                print(f'{password},{customer.password}')
                
                print(f'{flag}')    
        else:
          error_message = 'Contraseña o Email incorrecto !!'
        #print (email,password)
        return render(request,'login.html',{'error':error_message})
    
    def logout(request):
        request.session.clear()
        return redirect('login')
    
    
    
 
 
class Cart(View):
    def get(self,request):
        ids = list(request.session.get('cart').keys())
        productbyid = products.get_products_by_id(ids)
        return render(request,'cart.html',{'productbyid':productbyid})     
    
    def post(self, request):
        cart={}
        request.session['cart'] =cart
        total_items = sum(cart.values())
        request.session['total_items'] = total_items  
        request.session.modified = True
        return HttpResponseRedirect(reverse('cart'))



class CheckOut(View):
    
    #manda la orden
    def post(self,request):
        address = request.POST.get('address')
        calle = request.POST.get('calle')
        code_postal = request.POST.get('code_postal')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        productsitem = products.get_products_by_id(list(cart.keys()))
        
        print(address,code_postal, phone, customer, cart, productsitem,calle)
        
        for product in productsitem:
            print(cart.get(str(product.id)))
            orderitem = order(customer=Customer(id=customer),
                          product=product,
                          price=product.price,
                          address=address,
                          calle=calle,
                          code_postal=code_postal,
                          phone=phone,
                          quantity=cart.get(str(product.id)))
            orderitem.save()
        request.session['cart'] = {}
        return redirect('cart')
    
def get_addresses(request):
    postal_code = request.GET.get('code_postal')
    api_key = 'AIzaSyDYshbuU37TSIShLySGYxjP6bs4nMMPNx0' 
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    response = requests.get(f"{base_url}?components=postal_code:{postal_code}&key={api_key}")
    data = response.json()
    address = []
    # Itera a través de los resultados y extrae postcode_localities si están presentes
    for result in data['results']:
        # Algunos códigos postales pueden tener localidades asociadas directamente
        if 'postcode_localities' in result:
            address.extend(result['postcode_localities'])
        else:
            # Si no, intenta extraer la localidad de los componentes de la dirección
            locality_component = next(
                (component for component in result['address_components'] if 'locality' in component['types']), 
                None
            )
            if locality_component:
                address.append(locality_component['long_name'])
    
    

    print(f'postal code {postal_code}')
    print(f'address {address}')
    
    return JsonResponse(address, safe=False)


class OrderView(View):
    def get(self, request):
        customer = request.session.get('customer')
        orders = order.get_orders_by_customer(customer)
        print(f'this is the order{orders}')
        return render(request , 'orders.html'  , {'orders' : orders})