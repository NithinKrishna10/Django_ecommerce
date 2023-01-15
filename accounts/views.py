from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect,HttpResponseRedirect
import requests
from cart.models import CartItem,Cart
from cart.views import _cart_id
from orders.models import OrderProducts
from django.views.decorators.cache import never_cache
import datetime
from datetime import date, timedelta


from orders.models import Order, Orders
from .models import Account, UserProfile, Address,Return_request
from twilio.rest import Client
# from accounts.forms import UserAdminCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegistrationForm, UserForm, UserProfileForm, AddressForm
from django.contrib.sites.shortcuts import get_current_site
from xhtml2pdf import pisa
import xlwt
from django.template.loader import get_template
from .mixins import send_message, send_otp_on_phone
from django.contrib import messages

def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
                
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            if Account.objects.filter(phone_number=phone_number).exists():
                    print(phone_number)
                    
            else:
                user = Account.objects.create_user(
                        first_name=first_name, last_name=last_name, email=email, username=username, password=password)
                user.phone_number = phone_number
                user.save()
                # Create a user profile
                profile = UserProfile()
                profile.user_id = user.id
                profile.profile_picture = 'default/default-user.png'
                profile.email = email
                profile.phone_number = phone_number
                profile.save()
                
                return redirect('login_user')
    else:
        form = RegistrationForm()
        context = {
            'form': form,
        }
    return render(request, 'accounts/register.html', context)




def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    # Getting the product variations by cart id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                    # Get the cart items from the user to access his product variations
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    # product_variation = [1, 2, 3, 4, 6]
                    # ex_var_list = [4, 6, 3, 5]

                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                # next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('dashboarduser')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')


def signout(request):

    logout(request)
    # if 'username' in request.session:
    #     request.session.flush()
    # request.session.flush()

    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')


@login_required(login_url='login')
def edit_profile(request):
    try:
        userprofile = get_object_or_404(UserProfile, user=request.user)
        if request.method == 'POST':
            # user_form = UserForm(request.POST, instance=request.user)
            profile_form = UserProfileForm(
                request.POST, request.FILES, instance=userprofile)
            
            if profile_form.is_valid():
                # user_form.save()
                profile_form.save()
                messages.success(request, 'Your profile has been updated.')
                return redirect('edit_profile')
        else:
            user_form = UserForm(instance=request.user)
            profile_form = UserProfileForm(instance=userprofile)
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'userprofile': userprofile,
        }
        return render(request, 'accounts/edit_profile.html', context)
    except:
        pass

@login_required(login_url='login')
def dashboarduser(request):
   
    try:
        orders = Orders.objects.order_by(
            '-created_at').filter(user_id=request.user.id)
        orders_count = orders.count()

        print(orders_count)
        userprofile = UserProfile.objects.get(user_id=request.user.id)
        context = {
            'orders_count': orders_count,
            'userprofile': userprofile,
        }
    except:
        pass
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
def my_orders(request):
    try:
        orders = Orders.objects.filter(user=request.user).order_by('-created_at')
        ordersproducts = OrderProducts.objects.all()
        context = {
            'orders': orders,
            'ordersproducts' : ordersproducts
        }
        return render(request, 'accounts/my_orders.html', context)
    except:
        return render(request, 'accounts/my_orders.html')


@login_required(login_url='login')
def order_detail(request, order_id):
    try:
        order = Orders.objects.get(id=order_id)
        # num = order.order_number
        order_detail = OrderProducts.objects.filter(
            order_number=order.order_number)
        subtotal = 0

        for i in order_detail:
            subtotal += i.product_price * i.quantity

        print(subtotal)
        context = {
            'order_detail': order_detail,
            'order': order,
            'subtotal': subtotal,
        }
        return render(request, 'accounts/order_detail.html', context)
    except:
        pass


@login_required(login_url='login')
def cancel_order(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        order.status = 'Cancelled'
        order.save()

    return redirect('my_orders')


@login_required(login_url='login')
def orderproducts(request):

    orderitems = OrderProducts.objects.all()
    orders = Orders.objects.filter(user=request.user)

    context = {
        'orderitems': orderitems,
        'orders': orders,
    }

    return render(request, 'accounts/orderproducts.html', context)


def address_manage(request):
    try:

        address = Address.objects.filter(user=request.user)

        return render(request, 'accounts/address.html', {'address': address})
    except:
        pass

def add_address(request):
    try:
        if request.user.is_authenticated:
    
            if request.method == 'POST':
                user = request.user
                name = request.POST.get('first_name')  
                address1 = request.POST.get('address_line_1')
                address2 = request.POST.get('address_line_2')
                city = request.POST.get('city')
                phone1 = request.POST.get('phone1')
                phone2 = request.POST.get('phone2')
                state = request.POST.get('state')
                country = request.POST.get('country')
                pincode = request.POST.get('pincode')
                print(user)
                print(name)
                print(address1)
                print(address2)
                print(city)
                print(phone1)
                print(phone2)
                Address.objects.create(user=user,name=name,address1=address1,address2=address2,city=city,phone1=phone1,phone2=phone2,state=state,country=country,pincode=pincode)
                
                return redirect('address_manage')
            return render(request, 'accounts/add_address.html')
        else:
            return redirect('login_user')
    except:
        pass
 


#  =s=s=s=s=s=s=s=s=s=s=s=s=s=s=s===================== OTP LOGIN ==============s=s=s=s=s=s=s=s=s=s=s=s=s=s=s=s=s=s=s=s=s=s=

def cancelOrder(request):

    if request.method == 'POST':
        order_id = request.method.POST.get('order_id')
        order = Order.objects.get(id=order_id)
        order.status = 'Cancelled'
        order.save()
    return JsonResponse({'success': 'success'})


def sms_login(request):
    try:
        '''Gets user info for SMS based login'''
        if request.method == 'POST':
            global phone_number1
            phone_number1 = request.POST.get('phone_number')

            if Account.objects.filter(phone_number=phone_number1).exists():
                user = Account.objects.get(phone_number=phone_number1).email
                client = Client('AC1cb3556b8da7c50552bfa5acbe8136c0',
                                        'e08a6c38c2e9815753a5c3b8fd142442')
                verification = client.verify \
                        .v2 \
                        .services('VA5f01dd43040a12d2a12bae9bfc681ff0') \
                        .verifications \
                        .create(to='+91{}'.format(phone_number1), channel='sms')
                return render(request, 'accounts/otplogin.html')
            else:

                return render(request, 'accounts/smslogin.html', {'message': "invalid phone"})

        else:
            return render(request, 'accounts/smslogin.html')
    except:
        pass


def otp_login(request):
    try:
        '''Verifys and Logs in user with SMS OTP'''
        user = Account.objects.get(phone_number=phone_number1)
        if request.method == 'POST':
            Otp1 = request.POST.get('otp')
            client = Client('AC1cb3556b8da7c50552bfa5acbe8136c0',
                                'e08a6c38c2e9815753a5c3b8fd142442')
            verification_check = client.verify \
                    .v2 \
                    .services('VA5f01dd43040a12d2a12bae9bfc681ff0') \
                    .verification_checks \
                    .create(to='+91{}'.format(phone_number1), code=Otp1)

            print(verification_check.status, 'hai')
            if verification_check.status == 'approved':
                
                auth.login(request, user)
            else:
                messages.error(request, 'otp ithalla')
                return redirect('otplogin')

            return redirect('home')

        else:
            return render(request, 'accounts/otplogin.html')
    except:
        pass


def invoice_render_pdf_view(request, *args, **kwargs):
   subtotal = 0
   pk = kwargs.get('pk')
   order = get_object_or_404(Orders, pk=pk)
   order_detail = OrderProducts.objects.filter(order_number=order.order_number)
   for i in order_detail:

       subtotal += i.product_price * i.quantity

   template_path = 'accounts/invoice.html'
   context= {
        'order_detail': order_detail,
        'order': order,
        'subtotal': subtotal,
    }
   # Create a Django response object, and specify content_type as pdf
   response = HttpResponse(content_type='application/pdf')

   # to directly download the pdf we need attachment 
   # response['Content-Disposition'] = 'attachment; filename="report.pdf"'

   # to view on browser we can remove attachment 
   response['Content-Disposition'] = 'filename="report.pdf"'

   # find the template and render it.
   template = get_template(template_path)
   html = template.render(context)

   # create a pdf
   pisa_status = pisa.CreatePDF(
      html, dest=response)
   # if error then show some funy view
   if pisa_status.err:
      return HttpResponse('We had some errors <pre>' + html + '</pre>')
   return response

def return_order(request, order_id):
    '''handles the return request from the user'''
    if 'email' in request.session:
        email = request.session['email']
    else:
        return redirect('login_user')
    print(email)
    this_user = Account.objects.get(email=email)
    
    product = Orders.objects.get(id=order_id)
    if request.method == 'POST':
        # user = this_user.id
        reason = request.POST.get('reason')
        return_request = Return_request.objects.create(
            user=this_user, reason=reason,order_number = product.order_number)
        return_request.save()
        product.status = 'Return Requested'
        product.save()
        print('return request applied ')
        return redirect('home')
    return render(request, 'accounts/return_order.html', {'product': product})

