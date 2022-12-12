from email import message
from django.shortcuts import redirect, render

from .models import Product,Category,ProductAttribute

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
        # pro_atribute = ProductAttribute.objects.get(product = product_id, sizes = Small )
        # print(pro_atribute.quantinty)
        # product_variant = ProductAttribute.objects.get(pk=product_id)
        context = {
        'single_product': single_product,
        # 'product_variant': product_variant,
        }
        # variation = Variation
        # in_cart = CartItem.(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    # if request.user.is_authenticated:
    #     try:
    #         orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
    #     except OrderProduct.DoesNotExist:objects.filter
    #         orderproduct = None
    # else:
    #     orderproduct = None

    # Get the reviews
    # if single_product.variant !="None":
    #     Prod{uct have variants
      
    #     variants = ProductAttribute.objects.filter(product_id=id)
    #     colors = ProductAttribute.objects.filter(product_id=id,size_id=variants[0].size_id )
    #     sizes = ProductAttribute.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id',[id])
    #     variant =ProductAttribute.objects.get(id=variants[0].id)
    #     context.update({'sizes': sizes, 
    #                     'colors': colors,
    #                     'variant': variant,
    #                     })
    
  

    return render(request, 'store/productdetails.html', context)
