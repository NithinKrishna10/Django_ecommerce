from django.urls import reverse
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
# class Category(models.Model):
#     title=models.CharField(max_length=100)
#     slug=models.CharField(max_length=50)
#     created_at=models.DateTimeField

#     def __str__(self):
#         return self.title


# class Brand(models.Model):
#     title=models.CharField(max_length=50)


#     def __str__(self):
#         return self.title

# class Size(models.Model):
#     title=models.CharField(max_length=20)

#     def __str__(self):
#         return self.title

# class Color(models.Model):
#     title=models.CharField(max_length=50)
#     color_code=models.CharField(max_length=50)

#     def __str__(self):
#         return self.title


# class Product(models.Model):
#     title=models.CharField(max_length=50)
#     image=models.ImageField(upload_to='products')
#     slug=models.CharField(max_length=50)
#     decription=models.TextField()
#     category=models.ForeignKey(Category, on_delete=models.CASCADE)
#     brand=models.ForeignKey(Brand, on_delete=models.CASCADE)
#     size=models.ForeignKey(Size, on_delete=models.CASCADE)
#     color=models.ForeignKey(Color, on_delete=models.CASCADE)
#     status=models.BooleanField()

#     def __str__(self):
#         return self.title

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
    brand_description = models.TextField()
    brand_image = models.ImageField(upload_to='photos/brand', null=True)

    def __str__(self):
        return self.brand_name


class Product(models.Model):

    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    brand = models.ForeignKey(Brand, default=1, on_delete=models.CASCADE)
    gender = models.ForeignKey(Gender, default=1, on_delete=models.CASCADE)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug, self.pk])

    def __str__(self):
        return self.product_name


# class Size(models.Model):
#     size_num = models.CharField(max_length=10)

#     def __str__(self):
#        return self.size_num


# class Color(models.Model):
#     color_name = models.CharField(max_length=15)

# class ProductAttribute(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     sizes = models.ForeignKey(Size ,on_delete=models.CASCADE)
#     colors = models.ForeignKey(Color, null=True, blank=True,on_delete=models.CASCADE)
#     quantinty= models.IntegerField(default=0)

#     # def __str__(self):
#     #     return self.product
#     def img(self):
#         imag =  Product.objects.get(id= self.product)

        # if imag is not None:
        #      varimage=imag.images.url
        # else:
        #     varimage=""
        # return varimage

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
