from django.shortcuts import render
from requests import request
from accounts.models import Account
from cart.models import Cart
from store.models import Product, Category
from django.contrib.auth.models import User
from cart.models import CartItem


def home(request):
    

    global cart_count
    '''Render and control the datas in the user home page'''
    user = ''
    try:
        if 'user' in request.session:
            user_email = request.session['user']
            user = Account.objects.get(email=user_email)
            cart_count = Cart.objects.filter(user=user).count()
        else:
            user = 'guest'
            guest_id = request.COOKIES['sessionid']
            cart_count = Cart.objects.filter(guest_id=guest_id).count()
            
    except:
        pass
    # if request.user.is_authenticated:
    #     fname = User.first_name
                
    #     context = {
    #         'products': products,
    #         'cate' : cate,
    #     }
    #     return render(request, {"fname":fname},context)

    
    products = Product.objects.all().filter(is_available=True).order_by('created_date')
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

