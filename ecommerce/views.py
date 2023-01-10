from django.shortcuts import render
from requests import request
from accounts.models import Account
from cart.models import Cart
from store.models import Product, Category
from django.contrib.auth.models import User
from cart.models import CartItem

def home(request):
    

    products = Product.objects.all().filter(is_available=True,is_trending=True).order_by('created_date')
    cate = Category.objects.all()
    cart = CartItem.objects.filter(user_id=request.user.id)
    cart_count = cart.count()
    

    context = {
        
        'products': products,
        'cate' : cate,
        'cart' : cart,
        'cart_count' : cart_count,
    }
    return render(request, 'indexhome.html', context)
