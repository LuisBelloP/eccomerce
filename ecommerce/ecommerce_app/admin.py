from django.contrib import admin
from .models import category,products,customer,order
# Register your models here.

admin.site.register(category)
admin.site.register(products)
admin.site.register(customer)
admin.site.register(order)