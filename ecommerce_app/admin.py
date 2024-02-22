from django.contrib import admin
from .models import category,products,Customer,order
# Register your models here.

class Product_Admin(admin.ModelAdmin):
    list_display =('name','price','description','image','image_render','quantity','stripe_price_id')
    ##search_fields = ('')
    list_editable = ('price','image','description','quantity','stripe_price_id')
    

class Order_Admin(admin.ModelAdmin):
    list_display = ('product','product_image','quantity','code_postal','address','phone','date','status')
    readonly_fields=('product_image',)
    
    def product_image(self,obj):
        return obj.product_image
    product_image.short_description ='Product Image'
    product_image.allow_tags = True

admin.site.register(products,Product_Admin)
admin.site.register(category)
admin.site.register(Customer)
admin.site.register(order,Order_Admin)