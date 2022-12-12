from django.shortcuts import render
from store.models import Product,Category
from django.contrib.auth.models import User

def home(request):
    # if request.user.is_authenticated:
    #     fname = User.first_name
                
    #     context = {
    #         'products': products,
    #         'cate' : cate,
    #     }
    #     return render(request, {"fname":fname},context)

        
    products = Product.objects.all().filter(is_available=True).order_by('created_date')
    cate = Category.objects.all()
        # Get the reviews
        
    context = {
        'products': products,
        'cate' : cate,
    }
    return render(request, 'base.html', context)


