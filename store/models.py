from django.urls import reverse
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# ============================================================ #
class Gender(models.Model):
    gender = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.gender


class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    cat_image = models.ImageField(upload_to='photos/category')

    def __str__(self):
        return self.category_name


class Brand(models.Model):
    brand_name = models.CharField(max_length=200, unique=True)
    image = models.ImageField(upload_to='photos/brand', null=True)

    def __str__(self):
        return self.brand_name


class Product(models.Model):

    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    brand = models.ForeignKey(Brand, default=1, on_delete=models.CASCADE)
    gender = models.ForeignKey(Gender, default=1, on_delete=models.CASCADE)
    description = models.TextField(max_length=500, blank=True)
    offer_percentage = models.IntegerField(default=0,validators=[MaxValueValidator(70)])
    original_price= models.IntegerField(default=1, validators=[MinValueValidator(1)])
    price = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField(default=0)
    is_trending= models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug, self.pk])

    def __str__(self):
        return self.product_name

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)



variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value





