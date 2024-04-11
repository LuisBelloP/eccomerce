
from django.contrib import admin
from django.urls import path
from . import views
from .middlewares.auth import auth_middleware


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('',views.Index.as_view(),name='home'),
    path('store/',views.store,name='store'),
    
    path('contactus/',views.contactus, name='contactus'),
    path('term_privacy/',views.term_privacy, name='term_privacy'),
    
    path('aboutus/',views.aboutus, name='aboutus'),
    path('cart_empty',views.cart_empty,name='cartempty'),
    path('<int:id>/',views.Detail_view.as_view(),name='Detail_view'),
    path('signup/',views.Signup.as_view(),name='signup'),
    path('login/',views.Login.as_view(),name='login'),
    path('logout/',views.Login.logout,name='logout'),
    path('cart/',views.Cart.as_view(),name='cart'),
    path('create-checkout-session/', views.create_checkout_session, name='create-checkout-session'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('check-out/',views.CheckOut.as_view(),name='checkout'),
    path('get_addresses/', views.get_addresses, name='get_addresses'),
    path('orders/', auth_middleware(views.OrderView.as_view()), name='orders'),
    
    path('link1/',views.check_out_session_link,name="link1")
]