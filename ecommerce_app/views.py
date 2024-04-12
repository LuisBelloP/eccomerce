from django.shortcuts import render,redirect,HttpResponseRedirect,get_object_or_404,HttpResponse
import stripe.error
from .models import products,Customer,order
from django.contrib.auth.hashers import check_password,make_password
from django.views import View
from django.urls import reverse 

from googlemaps import Client as GoogleMaps
from django.conf import settings
from django.http import JsonResponse
import requests 
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


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
    #print (f'the products {products_to_post}')
    #print('you are : ', request.session.get('email'))
    return render(request,'index.html',{'products_to_post':products_to_post})

class Detail_view(View):
    
     def get(self,request,id):
        products_to_post = products.objects.get(id=id)
        return render(request,'view_details.html',{'products_to_post':products_to_post})



def aboutus(request):
    return render(request,'about_us.html')
def contactus(request):
    return render(request,'contact_us.html')
def term_privacy(request):
    return render(request,'term_privacy.html')
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

def cart_empty(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        for product_id, quantitys in cart.items():
            # Suponiendo que tienes un modelo de producto con un campo de 'stock'
            product = products.objects.get(id=product_id)
            product.quantity += quantitys  # Aumenta el stock del producto
            product.save()
        return HttpResponseRedirect(reverse('store')) 


class CheckOut(View):
    #manda la orden
    def post(self,request):
        address = request.POST.get('address')
        calle = request.POST.get('calle')
        num_interior = request.POST.get('num_int')
        code_postal = request.POST.get('code_postal')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        productsitem = products.get_products_by_id(list(cart.keys()))      
        for product in productsitem:
            #first step to rest product on admin panel 
            cart_quantity_product_model=cart.get(str(product.id))
            orderitem = order(customer=Customer(id=customer),
                          product=product,
                          price=product.price,
                          address=address,
                          calle=calle,
                          num_interior=num_interior,
                          code_postal=code_postal,
                          phone=phone,
                          quantity=cart.get(str(product.id))
                          )
            # second step to rest prodcut on admin panel 
            for _ in range(cart_quantity_product_model): 
                product.less()
                
            orderitem.save()
        return redirect('create-checkout-session')
    
def get_addresses(request):
    postal_code = request.GET.get('code_postal')
    #### key api
    api_key = settings.GOOGLE_MAPS_API_KEY
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
    return JsonResponse(address, safe=False)

@csrf_exempt
def create_checkout_session(request):
    stripe.api_key = settings.STRIPE_API_KEY
    cart = request.session.get('cart',{})
    line_items = []
    for product_id,quantity in cart.items():
        product= get_object_or_404(products,id=product_id)
        line_items.append(
            {
                'price':product.stripe_price_id,
                'quantity':quantity, 
            }
        )
    if request.method == 'POST':
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=line_items,
                mode='payment',
                success_url=request.build_absolute_uri(reverse('payment_success')),
                cancel_url=request.build_absolute_uri(reverse('cart')),
            )
            return JsonResponse({'id':checkout_session.id})
        except Exception as e:
            print(e)  
        return JsonResponse({'error': str(e)}, status=400)
        
    if request.method == 'GET':
        ids = list(request.session.get('cart').keys())
        productbyid = products.get_products_by_id(ids)
        return render (request,'pay_method.html',{'productbyid':productbyid})


class OrderView(View):
    def get(self, request):
        customer = request.session.get('customer')
        orders = order.get_orders_by_customer(customer)
        #print(f'this is the order{orders}')
        return render(request , 'orders.html'  , {'orders' : orders})
    
    
def payment_success(request):
    if 'cart' in request.session:
        del request.session['cart']
    
    return redirect('orders')


##################################### Stripe Links products

@csrf_exempt
def check_out_session_link(request,id):
    if request.method == "GET" or request.method == "POST":
        session = create_stripe_session_link(id)
        
        if request.method == "GET":
            return HttpResponseRedirect(session.url)
        else:
            return JsonResponse({'url':session.url})

def get_price(id):
    dictionary_price = {
       10:"price_1OanB5LtLKOujhTJQhb5RzSM",
       12:"price_1OanB5LtLKOujhTJQhb5RzSM",
       14:"price_1OanB5LtLKOujhTJQhb5RzSM",
       15:"price_1OanB5LtLKOujhTJQhb5RzSM",
       17:"price_1OanB5LtLKOujhTJQhb5RzSM",
       18:"price_1OanB5LtLKOujhTJQhb5RzSM",
       19:"price_1OanB5LtLKOujhTJQhb5RzSM",
       20:"price_1OanB5LtLKOujhTJQhb5RzSM",
       21:"price_1OanB5LtLKOujhTJQhb5RzSM",
       22:"price_1OanB5LtLKOujhTJQhb5RzSM",
       23:"price_1OanB5LtLKOujhTJQhb5RzSM",
       24:"price_1OmOnYLtLKOujhTJS0SMFIFk",
       25:"price_1OmOnYLtLKOujhTJS0SMFIFk",
       26:"price_1OmOmJLtLKOujhTJfPegBx6Y",
       27:"price_1OmOmJLtLKOujhTJfPegBx6Y",
       28:"price_1OmOmJLtLKOujhTJfPegBx6Y",
       29:"price_1OmOmJLtLKOujhTJfPegBx6Y",
       30:"price_1OmOmJLtLKOujhTJfPegBx6Y",
       31:"price_1OmNnQLtLKOujhTJNr5Gkhxz",
       32:"price_1OmNnQLtLKOujhTJNr5Gkhxz",
       33:"price_1OqbqFLtLKOujhTJy70gftaP",
       34:"price_1OqbqFLtLKOujhTJy70gftaP",
       35:"price_1OmOmJLtLKOujhTJfPegBx6Y",
       36:"price_1OmOnYLtLKOujhTJS0SMFIFk",
       37:"price_1OmOnYLtLKOujhTJS0SMFIFk",
       38:"price_1OmOmJLtLKOujhTJfPegBx6Y",
       39:"price_1Owp6CLtLKOujhTJLirmtcpe",
       40:"price_1Owp6CLtLKOujhTJLirmtcpe",
       41:"price_1OqbqFLtLKOujhTJy70gftaP",
       42:"price_1P48akLtLKOujhTJct02lsR5",
       43:"price_1OmOmJLtLKOujhTJfPegBx6Y",
       44:"price_1OqbqFLtLKOujhTJy70gftaP",
    }
    
    return dictionary_price.get(id,"price_1OanB5LtLKOujhTJQhb5RzSM")

def create_stripe_session_link(id):
    stripe.api_key = settings.STRIPE_API_KEY
    
    price = get_price(id)
        
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': price,
            'quantity':1,
        }],
        mode='payment',
        success_url="https://usadelivery.onrender.com/",
        cancel_url="https://usadelivery.onrender.com/",
        shipping_address_collection={'allowed_countries':["MX"]},
        phone_number_collection={"enabled": True},
        custom_text={
            "shipping_address":{
                "message":
                "Please note that we can't"
            },
            "":{},
            "submit":{ "message":"we'll email your instructions on hot to get started"},
            "after_submit": {
                "message":
                "Learn more about **your purchase** on our [product page](https://usadelivery.onrender.com/).",
            },
        },
        metadata={'product_id': id },  
    )
    return session


@require_POST
@csrf_exempt


def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_API_KEY
    
    signature_header = request.META['HTTP_STRIPE_SIGNATURE']
    payload = request.body
    endpoint_secret = 'firma secreta de webhook'
    
    try:
        event = stripe.Webhook.construct_event(
            payload,signature_header,endpoint_secret
        )
    except ValueError as e:
        
        
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        
        
        return HttpResponse(status=400)
    
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        product_id = session.get('metadata').get('product_id')
        
        print(session)
        print(product_id)
        
        less_quantity(product_id,products)
        
    return HttpResponse(status=200)


def less_quantity(id,model):
    elements = model.get(id)
    
    if elements.id == id:
        elements.quantity -1
        elements.save()
        return elements
    
