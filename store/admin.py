from django.contrib import admin
from store.models import Product, VariationProduct

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('product_name',)}
    list_display = ('product_name', 'slug', 'price', 'stock', 'category', 'modefied_at', 'is_available')

class VariationAdmin(admin.ModelAdmin):
    list_display    = ( 'product' , 'category_name', 'category_value', 'is_active' )
    list_editable   = ('is_active', )
    list_filter     = ('product' , 'category_name', 'category_value' )

admin.site.register(Product, ProductAdmin)
admin.site.register(VariationProduct, VariationAdmin)