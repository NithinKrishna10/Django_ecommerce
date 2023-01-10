from django.db import models
from accounts.models import Account,Address
from store.models import Product, Variation
import datetime
# from datetime import datetime

current_date = datetime.date.today()



class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    # payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100) # this is the total amount paid
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id


class Order(models.Model):
    STATUS = (
        
        ('Placed', 'Placed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )
    order_number = models.CharField(max_length=20)
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    pincode=models.IntegerField()
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='Placed')
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'

    def __str__(self):
        return self.first_name


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    order_number = models.CharField(default=1,max_length=20)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    is_ordered = models.BooleanField(default=False)
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name
    
    # ================================================================
    
    
    
    
    
    
     
class Orders(models.Model):
    STATUS = (
        
        ('Placed', 'Placed'),
        ('Shipped', 'Shipped'),
        ('Out For Delivery', 'Out For Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )
    order_number = models.CharField(max_length=20)
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    Shipping = models.ForeignKey(Address, on_delete=models.CASCADE)
    
    order_total = models.FloatField()
    tax = models.FloatField()
    payment_mode= models.CharField(max_length=150, null=False,default="Pending")
    payment_id= models.CharField(max_length=250, null=False,default=0)
    status = models.CharField(max_length=50, choices=STATUS, default='Placed')
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    Order_day  = models.IntegerField(default = current_date.day)
    Order_month  = models.IntegerField(default = current_date.month)
    Order_year  = models.IntegerField(default = current_date.year)
    def __str__(self):
            return self.order_number
    
    

class OrderProducts(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    order_number = models.CharField(default=1,max_length=20)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    is_ordered = models.BooleanField(default=False)
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name
    
class Product_Return(models.Model):
    order_num =models.CharField(max_length=100)
    user = models.ForeignKey(Account,on_delete = models.CASCADE)
    reason = models.CharField(max_length = 500)


