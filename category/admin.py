from django.contrib import admin
from category.models import Category

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('category_name',)}
    list_display = ('category_name', 'slug', 'cat_image','created_at')
# Register your models here.
admin.site.register(Category,CategoryAdmin)