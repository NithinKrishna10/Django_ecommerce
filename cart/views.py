from django.shortcuts import get_object_or_404, render, redirect

from  accounts.models import UserProfile,Address
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http.response import JsonResponse
from store.models import Product
# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


# def update_cart(request):
    


def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)  # get the product
    # If the user is authenticated
    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(
                        product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)

                except:
                    pass

        is_cart_item_exists = CartItem.objects.filter(
            product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(
                product=product, user=current_user)
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                if item.quantity < product.stock:
                    print(product.stock)
                    item.quantity += 1
                    item.save()
                else:
                    messages.error(request, "No stock available !!")
                    return redirect('cart')

            else:
                item = CartItem.objects.create(
                    product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=current_user,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')
    # If the user is not authenticated
    else:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(
                        product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        try:
            # get the cart using the cart_id present in the session
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(
            product=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            # existing_variations -> database
            # current variation -> product_variation
            # item_id -> database
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            print(ex_var_list)

            if product_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                if item.quantity < product.stock:
                    print(product.stock) 
                    item.quantity += 1
                    item.save()
                    messages.success(request, "No stock!!")
                    return redirect('cart')
            else:
                item = CartItem.objects.create(
                    product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        # print(cart_item.variations.all)
        return redirect('cart')


def remove_cart(request,  cart_item_id):

    # product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(
                 user=request.user, id=cart_item_id)
            print(cart_item.variations)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(
                 cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass

    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(
            product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(
            product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')




def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            userpro =UserProfile.objects.filter(
                user=request.user)
            addresses =Address.objects.filter(
                user=request.user)
            cart_items = CartItem.objects.filter(
                user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass  # just ignore

    context = {
        'addresses' : addresses,
        'userpro' : userpro,
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)


@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            addresses =Address.objects.filter(
                user=request.user)
            userpro =UserProfile.objects.filter(
                user=request.user)
            cart_items = CartItem.objects.filter(
                user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (5 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    
    context = {
        'addresses' : addresses,
        'userpro' : userpro,
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/checkout.html', context)


def updatecart(request):
    
    # if request.method == 'POST':
    #     prod_id = int(request.POST.get('product_id'))
    #     if(CartItem.objects.filter(user=request.user,product_id=prod_id)):
    #         prod_qty = int(request.POST.get('product_qty'))
    #         cart = CartItem.objects.get(product_id=prod_id, user=request.user)
    #         cart.quantity = prod_qty
    #         cart.save()
    #         return JsonResponse({'status': "Update success"})
    # return redirect('/')
    
    user = 'guest'
    if 'user' in request.session:
        user = request.session['user']
    else:
        guest_id = request.COOKIES['sessionid']

    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        cart_id = request.POST.get('cart_id')
        task = request.POST.get('task')
        print(task)
        try:
            user = Account.objects.get(email=user)
        except:
            user = guest_id

        product = CartItem.objects.get(id=cart_id)
        
        stock = Product.objects.get(id=product.product.id)
        print(stock.brand)
  
        stock_balance = stock.stock
        print(product.quantity)
        print('got quantity', quantity)
        if task == 'plus':
            # updated_quantity = int(quantity) + 1
            if product.quantity < stock.stock :
               product.quantity += 1
               product.save()
            else:
                pass
            print(product.quantity)
            if stock_balance > 1:
                product.quantity = updated_quantity
                print('updated quantity', updated_quantity)
                # stock manage
                stock.stock = stock.stock - 1
            else:
                updated_quantity = quantity
        else:
            # updated_quantity = quantity - 1
            if product.quantity >    1 :
               product.quantity -= 1
               product.save()           
            
            if updated_quantity >= 1:
                product.quantity = updated_quantity
                print('updated quantity', updated_quantity)
                # stock manage
                stock.stock = stock.stock + 1
            else:
                updated_quantity = quantity
      
        # product.save()
   
        
        print('saved the changes in database')
        return JsonResponse({
            'updated_quantity': updated_quantity,
            'stock': stock.stock,
            # 'total_price': product.total_price,
            
            
        })
    return JsonResponse({'user': 'user_info'})