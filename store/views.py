from email import message
from django.shortcuts import redirect, render

from cart.models import CartItem

from .models import Product,Category

# Create your views here.

# def product_detail(request, id, product_slug):
   
# #    if(Category.objects.filter(slug=category_slug, status=0)):
# #        if(Product.objects.filter(slug=product_slug , status=0)):
# #            products =Product.objects.filter(slug=product_slug, status=0).first
# #            context={ 'products': products }
# #        else:
# #            message.error(request, "no")
# #            return redirect('home')


#     product = Product.objects.get(pk=id)  
#     context={
#         'product': product
#     }
#     return render(request, 'store/productdetail.html', context)

def store_view(request):
    products = Product.objects.all().filter(is_available=True).order_by('created_date')
    cate = Category.objects.all()
        # Get the reviews

    context = {
        'products': products,
        'cate' : cate,
    }
    
    return render(request, 'store/storev.html', context)

    
    
def product_detail(request, category_slug, product_slug, product_id):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        cartitem = CartItem.objects.filter(product=single_product).exists()
        print(cartitem)
        # in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e
    
   
    context = {
        'single_product': single_product,
        'cartitem': cartitem
        # 'in_cart'       : in_cart,
        # 'orderproduct': orderproduct,
        # 'reviews': reviews,
        # 'product_gallery': product_gallery,
    }
    return render(request, 'store/productdetail.html', context)

