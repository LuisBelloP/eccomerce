
from django.contrib import admin
from django.urls import path
from . import views
from .middlewares.auth import auth_middleware


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('',views.Index.as_view(),name='home'),
    path('store/',views.store,name='store'),
    
    path('aboutus/',views.aboutus, name='aboutus'),
    path('<int:id>/',views.detail_view,name='detail_view'),
    path('signup/',views.Signup.as_view(),name='signup'),
    path('login/',views.Login.as_view(),name='login'),
    path('logout/',views.Login.logout,name='logout'),
    path('cart/',views.Cart.as_view(),name='cart'),
    
    path('check-out/',views.CheckOut.as_view(),name='checkout'),
    path('orders/', auth_middleware(views.OrderView.as_view()), name='orders'),
]