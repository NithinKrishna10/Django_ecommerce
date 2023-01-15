from email import message
from django.shortcuts import redirect, render

from cart.models import CartItem

from .models import Product,Category,Gender,Brand,Variation
from django.db.models import Q
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

# Create your views here.


def store_view(request):
    products = Product.objects.all().filter(is_available=True).order_by('created_date')
    cate = Category.objects.all()
    gender = Gender.objects.all()
    brand = Brand.objects.all()
    variation = Variation.objects.all()
    products_paginater = Paginator(products,8)
    
    # page_num = request.GET.get('page')
    
    # page = products_paginater.get_page(page_num)
    
        # Get the reviews
    page_number = request.GET.get('page')
    try:
        page_obj = products_paginater.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = products_paginater.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = products_paginater.page(products_paginater.num_pages)
    context = {
        'page_obj': page_obj,
        'variation':variation,
        'brand': brand,
        # 'products': products,
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
    brand = Brand.objects.all()
            # Get the reviews
    products_paginater = Paginator(products,8)
    
    # page_num = request.GET.get('page')
    
    # page = products_paginater.get_page(page_num)
    
        # Get the reviews
    page_number = request.GET.get('page')
    try:
        page_obj = products_paginater.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = products_paginater.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = products_paginater.page(products_paginater.num_pages)
    context = {
         'page_obj': page_obj,
            'brand' : brand,
            'products': products,
            'cate' : cate,
            'gender' : gender,
        }
    
    return render(request, 'store/storev.html', context)

def brand_view(request,brand_id):
    
        # brand_id = int(request.POST.get('brand_id'))
    brands = Brand.objects.get(id = brand_id)
    print(brands.brand_name)
    products = Product.objects.all().filter(is_available=True,brand=brands).order_by('created_date')
    cate = Category.objects.all()
    brand = Brand.objects.all()
    gender = Gender.objects.all()
            # Get the reviews
    products_paginater = Paginator(products,8)
    
    # page_num = request.GET.get('page')
    
    # page = products_paginater.get_page(page_num)
    
        # Get the reviews
    page_number = request.GET.get('page')
    try:
        page_obj = products_paginater.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = products_paginater.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = products_paginater.page(products_paginater.num_pages)
    context = {
         'page_obj': page_obj,
            'products': products,
            'cate' : cate,
            'brand' : brand,
            'gender' : gender,
        }
    
    return render(request, 'store/storev.html',context)


def price_filter(request,brand_id):
    
        # brand_id = int(request.POST.get('brand_id'))
    brands = Brand.objects.get(id = brand_id)
    print(brands.brand_name)
    products = Product.objects.all().filter(is_available=True,brand=brands).order_by('created_date')
    cate = Category.objects.all()
    brand = Brand.objects.all()
    gender = Gender.objects.all()
            # Get the reviews
    products_paginater = Paginator(products,8)
    
    # page_num = request.GET.get('page')
    
    # page = products_paginater.get_page(page_num)
    
        # Get the reviews
    page_number = request.GET.get('page')
    try:
        page_obj = products_paginater.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = products_paginater.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = products_paginater.page(products_paginater.num_pages)
    context = {
         'page_obj': page_obj,
            'products': products,
            'cate' : cate,
            'brand' : brand,
            'gender' : gender,
        }
    
    return render(request, 'store/storev.html',context)



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
    return render(request, 'store/search.html', context)


def price_filter(request):
    products = Product.objects.all()
    min_price = request.GET.get('min_price', None)
    max_price = request.GET.get('max_price', None)
    if min_price and max_price:
        products = products.filter(price__range=(min_price, max_price))
    elif min_price:
        products = products.filter(price__gte=min_price)
    elif max_price:
        products = products.filter(price__lte=max_price)
    cate = Category.objects.all()
    brand = Brand.objects.all()
    gender = Gender.objects.all()
            # Get the reviews
    products_paginater = Paginator(products,8)
    
    # page_num = request.GET.get('page')
    
    # page = products_paginater.get_page(page_num)
    
        # Get the reviews
    page_number = request.GET.get('page')
    try:
        page_obj = products_paginater.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = products_paginater.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = products_paginater.page(products_paginater.num_pages)
        
        
    context = {
            'page_obj': page_obj,
            'products': products,
            'cate' : cate,
            'brand' : brand,
            'gender' : gender,
            'products': products
        }
    
    return render(request, 'store/storev.html', context)


def price_high(request):
    products = Product.objects.all().filter(is_available=True).order_by('-price')
    cate = Category.objects.all()
    gender = Gender.objects.all()
    brand = Brand.objects.all()
    variation = Variation.objects.all()
    products_paginater = Paginator(products,8)
    
    # page_num = request.GET.get('page')
    
    # page = products_paginater.get_page(page_num)
    
        # Get the reviews
    page_number = request.GET.get('page')
    try:
        page_obj = products_paginater.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = products_paginater.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = products_paginater.page(products_paginater.num_pages)
    context = {
        'page_obj': page_obj,
        'variation':variation,
        'brand': brand,
        # 'products': products,
        'cate' : cate,
        'gender' : gender,
    }
    
    return render(request, 'store/storev.html', context)



def price_low(request):
    products = Product.objects.all().filter(is_available=True).order_by('price')
    cate = Category.objects.all()
    gender = Gender.objects.all()
    brand = Brand.objects.all()
    variation = Variation.objects.all()
    products_paginater = Paginator(products,8)
    
    # page_num = request.GET.get('page')
    
    # page = products_paginater.get_page(page_num)
    
        # Get the reviews
    page_number = request.GET.get('page')
    try:
        page_obj = products_paginater.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = products_paginater.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = products_paginater.page(products_paginater.num_pages)
    context = {
        'page_obj': page_obj,
        'variation':variation,
        'brand': brand,
        # 'products': products,
        'cate' : cate,
        'gender' : gender,
    }
    
    return render(request, 'store/storev.html', context)



def newest(request):
    products = Product.objects.all().filter(is_available=True).order_by('-created_date')
    cate = Category.objects.all()
    gender = Gender.objects.all()
    brand = Brand.objects.all()
    variation = Variation.objects.all()
    products_paginater = Paginator(products,8)
    
    # page_num = request.GET.get('page')
    
    # page = products_paginater.get_page(page_num)
    
        # Get the reviews
    page_number = request.GET.get('page')
    try:
        page_obj = products_paginater.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = products_paginater.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = products_paginater.page(products_paginater.num_pages)
    context = {
        'page_obj': page_obj,
        'variation':variation,
        'brand': brand,
        # 'products': products,
        'cate' : cate,
        'gender' : gender,
    }
    
    return render(request, 'store/storev.html', context)



def offer_high(request):
    products = Product.objects.all().filter(is_available=True).order_by('-offer_percentage')
    cate = Category.objects.all()
    gender = Gender.objects.all()
    brand = Brand.objects.all()
    variation = Variation.objects.all()
    products_paginater = Paginator(products,8)
    
    # page_num = request.GET.get('page')
    
    # page = products_paginater.get_page(page_num)
    
        # Get the reviews
    page_number = request.GET.get('page')
    try:
        page_obj = products_paginater.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = products_paginater.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = products_paginater.page(products_paginater.num_pages)
    context = {
        'page_obj': page_obj,
        'variation':variation,
        'brand': brand,
        # 'products': products,
        'cate' : cate,
        'gender' : gender,
    }
    
    return render(request, 'store/storev.html', context)
