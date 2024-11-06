from django.contrib import admin

from .models import Product


# Register your models here.



class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','price_public', 'stock', 'category','modified_date')
    prepopulated_fields= {'slug':('product_name',)}
    readonly_fields = ('price_public',)

admin.site.register(Product, ProductAdmin)
