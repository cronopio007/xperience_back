from django.db import models
from category.models import Category
from django.urls import reverse


# Create your models here.
# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=1000, blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='fotos/productos')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateField(auto_created=True)
    modified_date = models.DateField(auto_created=True)

    @property
    def price_public(self):
        return int(self.price * 1.25) if self.price is not None else 0


    def get_url(self):
        # product_detail es el nombre que se le pone el urls.py
        # reverse arma la url q se pasara con los argumentos
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name