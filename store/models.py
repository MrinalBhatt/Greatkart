from django.db import models
from category.models import Category
from django.urls import reverse

# Create your models here.
class Product(models.Model):
    product_name         = models.CharField(max_length = 200, unique= True)
    slug                = models.SlugField(max_length= 100, unique= True)
    description         = models.TextField(max_length=500, blank=True)
    price               = models.IntegerField()
    image               = models.ImageField(upload_to="photoes/products")
    stock               = models.IntegerField()
    is_available        = models.BooleanField(default = True)    
    category            = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at          = models.DateTimeField(auto_now_add= True)
    modefied_at         = models.DateTimeField(auto_now=True)

    def get_product_urls(self):
        return reverse('product_detail', args = [self.category.slug, self.slug,]) 


    def __str__(self):
        return self.product_name

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(category_name = 'color')
    def size(self):
        return super(VariationManager, self).filter(category_name = 'size')

category_name_select = (
    ('color', 'Color'),
    ('size', 'Size'),

)

class VariationProduct(models.Model):
    product             = models.ForeignKey(Product,on_delete=models.CASCADE)
    category_name       = models.CharField(max_length=100, choices=category_name_select)
    category_value      = models.CharField(max_length=100)
    is_active           = models.BooleanField(default=True)
    craeted_at          = models.DateTimeField(auto_now_add= True)
    updated_at          = models.DateTimeField(auto_now = True)

    object              = VariationManager()

    def __str__(self):
        return self.category_value
