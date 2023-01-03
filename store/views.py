from email import message
from django.shortcuts import redirect, render

from cart.models import CartItem

from .models import Product,Category,Gender,Brand
from django.db.models import Q
# Create your views here.


def store_view(request):
    products = Product.objects.all().filter(is_available=True).order_by('created_date')
    cate = Category.objects.all()
    gender = Gender.objects.all()
    brand = Brand.objects.all()
        # Get the reviews

    context = {
        'brand': brand,
        'products': products,
        'cate' : cate,
        'gender' : gender,
    }
    
    return render(request, 'store/storev.html', context)

    
    
def product_detail(request, category_slug, product_slug, product_id):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        cartitem = CartItem.objects.filter(product=single_product).exists()
        print(cartitem)
       
    except Exception as e:
        raise e
    
   
    context = {
        'single_product': single_product,
        'cartitem': cartitem
 
    }
    return render(request, 'store/productdetail.html', context)

def gender_view(request,gender_id):
    
        # gender_id = int(request.POST.get('gender_id'))
    gen = Gender.objects.get(id = gender_id)
    print(gen.gender)
    products = Product.objects.all().filter(is_available=True,gender=gen).order_by('created_date')
    cate = Category.objects.all()
    gender = Gender.objects.all()
            # Get the reviews

    context = {
            'products': products,
            'cate' : cate,
            'gender' : gender,
        }
    
    return render(request, 'store/storev.html', context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword) )
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/storev.html', context)
