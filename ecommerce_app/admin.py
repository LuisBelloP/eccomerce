from django.contrib import admin
from .models import category,products,customer,order
# Register your models here.

class Product_Admin(admin.ModelAdmin):
    list_display =('name','price','description','image')
    ##search_fields = ('')
    list_editable = ('price','image','description')
    

## class Order_Admin(admin.ModelAdmin):
## list_display = ('','','')
##  list_editable= ('products')
## Need function for diverse orders right
##admin.site.register(order,orderAdmin)


admin.site.register(products,Product_Admin)
admin.site.register(category)
admin.site.register(customer)
admin.site.register(order)