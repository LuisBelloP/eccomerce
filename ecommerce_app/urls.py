
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('<int:id>/',views.detail_view,name='detail_view'),
    path('signup/',views.Signup.as_view(),name='signup'),
]