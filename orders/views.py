
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from cart.models import CartItem,Cart
from accounts.models import Address
from .forms import OrderForm
import datetime
from .models import Order, Payment, OrderProduct,Orders
import json
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string



# def place_order(request, total=0, quantity=0,):
#     current_user = request.user
#     shipping_address_id = request.POST['shipping_address']
#     shipping_address = Address.objects.get(id=shipping_address_id)
#     # If the cart count is less than or equal to 0, then redirect back to shop
#     cart_items = CartItem.objects.filter(user=current_user)
#     cart_count = cart_items.count()
#     if cart_count <= 0:
#         return redirect('store')

#     grand_total = 0
#     tax = 0
#     for cart_item in cart_items:
#         total += (cart_item.product.price * cart_item.quantity)
#         quantity += cart_item.quantity
#     tax = (2 * total)/100
#     grand_total = total + tax

#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         print(OrderForm.errors)
#         if form.is_valid():
#             # Store all the billing information inside Order table
#             data = Order()
#             data.user = current_user
#             data.first_name = form.cleaned_data['first_name']
#             data.last_name = form.cleaned_data['last_name']
#             data.phone = form.cleaned_data['phone']
#             data.email = form.cleaned_data['email']
#             data.address_line_1 = form.cleaned_data['address_line_1']
#             data.address_line_2 = form.cleaned_data['address_line_2']
#             data.pincode =form.cleaned_data['pincode']
#             data.country = form.cleaned_data['country']
#             data.state = form.cleaned_data['state']
#             data.city = form.cleaned_data['city']
#             data.order_note = form.cleaned_data['order_note']
#             data.order_total = grand_total
#             data.tax = tax
            
#             data.ip = request.META.get('REMOTE_ADDR')
#             data.save()
#             # Generate order number
#             yr = int(datetime.date.today().strftime('%Y'))
#             dt = int(datetime.date.today().strftime('%d'))
#             mt = int(datetime.date.today().strftime('%m'))
#             d = datetime.date(yr,mt,dt)
#             current_date = d.strftime("%Y%m%d") #20210305
#             order_number = current_date + str(data.id)
#             data.order_number = order_number
#             data.save()
# # ===================================================================================================================
#         order = Order.objects.get(user=request.user, is_ordered=False)
#         order.is_ordered = True
#         order.save()

#         cart_items = CartItem.objects.filter(user=request.user)

#         for item in cart_items:
            
 
#             orderproduct=OrderProduct()
#             orderproduct.order_id = order.id
#             orderproduct.order_number = order.order_number 
#                 #orderproduct.payment = payment
#             orderproduct.user_id = request.user.id
#             orderproduct.product_id = item.product_id
#             orderproduct.quantity = item.quantity
#             orderproduct.product_price = item.product.price
#             orderproduct.ordered = True
            
#             orderproduct.save()

#             cart_item = CartItem.objects.get(id=item.id)
#             product_variation= cart_item.variations.all()
#             orderproduct = OrderProduct.objects.get(id=orderproduct.id)
#             orderproduct.variations.set(product_variation)
#             orderproduct.save()


#                 # Reduce the quantity of the sold products
#             product = Product.objects.get(id=item.product_id)
#             product.stock -= item.quantity
#             product.save()

#         # Clear cart
#         CartItem.objects.filter(user=request.user).delete()
#         # else:
#         return redirect('orsu') 
#         #     return redirect()


# ===================================================================================================================
            # # order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            # context = {
            #     'order': order,
            #     'cart_items': cart_items,
            #     'total': total,
            #     'tax': tax,
            #     'grand_total': grand_total,
            # }
            # return render(request, 'orders/payments.html', context)
    # else:
    #     return redirect('my_order')

# ===================== payment =======================

def orsu(request):
    
     return render(request,'orders/ordersucsess.html')




def order_complete(request):
    order_number = request.GET.get('order_number')
    # transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order =order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        # payment = Payment.objects.get(payment_id=transID)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            # 'transID': payment.payment_id,
            # 'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'orders/order_complete.html', context)
    except (Order.DoesNotExist):
        return redirect('home')



def place_order(request, total=0, quantity=0):
    current_user = request.user
    
    # shipping_address_id = request.POST['shipping_address']
    # shipping_address = Address.objects.get(id=shipping_address_id)
    # If the cart count is less than or equal to 0, then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = total + tax

    if request.method == 'POST':
        shipping_address_id = request.POST['shipping_address']
        shipping_address = Address.objects.get(id=shipping_address_id)
        # form = OrderForm(request.POST)
  
        data = Orders()
        data.user = current_user
        data.Shipping = shipping_address
        data.order_total = grand_total
        data.tax = tax
        data.payment_id = request.POST['payment_id']
        data.payment_mode =request.POST['payment_mode']
        # data.ip = request.META.get('REMOTE_ADDR')
        data.save()
            # Generate order number
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr,mt,dt)
        current_date = d.strftime("%Y%m%d") #20210305
        order_number = current_date + str(data.id)
        data.order_number = order_number
        
        data.save()
# ===================================================================================================================
        order = Orders.objects.get(user=request.user, is_ordered=False)
        order.is_ordered = True
        order.save()

        cart_items = CartItem.objects.filter(user=request.user)

        for item in cart_items:
            
 
            orderproduct=OrderProduct()
            orderproduct.order_id = order.id
            orderproduct.order_number = order.order_number 
                #orderproduct.payment = payment
            orderproduct.user_id = request.user.id
            orderproduct.product_id = item.product_id
            orderproduct.quantity = item.quantity
            orderproduct.product_price = item.product.price
            orderproduct.ordered = True
            
            orderproduct.save()

            cart_item = CartItem.objects.get(id=item.id)
            product_variation= cart_item.variations.all()
            orderproduct = OrderProduct.objects.get(id=orderproduct.id)
            orderproduct.variations.set(product_variation)
            orderproduct.save()


                # Reduce the quantity of the sold products
            product = Product.objects.get(id=item.product_id)
            product.stock -= item.quantity
            product.save()

        # Clear cart
        CartItem.objects.filter(user=request.user).delete()
        # else:
        payMode = request.POST['payment_mode']
        if (payMode == 'Paid by Razorpay'):
            return JsonResponse({'status' : "Your order placed"})
        
        
        
        return redirect('orsu') 
        #     return redirect()


def razorpaycheck(request):
    
    cart = CartItem.objects.filter(user=request.user)
    grand_total =0
    tax=0
    total=0
    quantity =0
    for item in cart:
        total += (item.product.price * item.quantity)
        quantity += item.quantity
        tax = (2 * total)/100
        grand_total = total + tax

    print(grand_total)
    return JsonResponse({
        'grand_total' : grand_total
    })