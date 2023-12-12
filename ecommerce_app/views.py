from django.shortcuts import render,redirect,HttpResponseRedirect
from .models import products,Customer
from django.contrib.auth.hashers import check_password,make_password
from django.views import View
# Create your views here.


class Index(View):
    
    def post(self,request):
        product = request.POST.get()
        remove = request.POST.get()
        cart = request.session.get()
        
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <=1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity -1
                else:  
                    cart[product] = quantity +1  
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        
        print('cart' , request.session['cart'])
        return redirect('home')
    
    def get(self,request):
        return 

def store (request):
    
    products_to_post = products.get_all_products()
    print('you are : ', request.session.get('email'))
    return render(request,'index.html',{'products_to_post':products_to_post})

### detail view products
def detail_view(request,id):
    products_to_post = products.objects.get(id=id)
    return render(request,'view_details.html',{'products_to_post':products_to_post})

def aboutus(request):
    return render(request,'about_us.html')

class Signup(View):
    def  get(self,request):
        return render(request,'sign_up.html')
   
    ##### function to coneect to formulario
    ### error in hash the password was because the parameter password was bad reference.
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
                error_message = 'Invalid etapa 2!!'
                print(f'{password},{customer.password}')
                
                print(f'{flag}')    
        else:
          error_message = 'Invalid etapa 1 !!'
        print (email,password)
        return render(request,'login.html',{'error':error_message})
    
    def logout(request):
        request.session.clear()
        return redirect('login')
    
    
    
    
    

