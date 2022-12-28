from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from orders.models import OrderProducts

import datetime
from datetime import date, timedelta



from orders.models import Order, Orders
from .models import Account, UserProfile,Address
from twilio.rest import Client
# from accounts.forms import UserAdminCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegistrationForm, UserForm, UserProfileForm, AddressForm
from django.contrib.sites.shortcuts import get_current_site
from .mixins import send_message, send_otp_on_phone


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
            user = Account.objects.create_user(
                first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()

            # Create a user profile
            profile = UserProfile()
            profile.user_id = user.id
            profile.profile_picture = 'default/default-user.png'
            profile.save()

            # USER ACTIVATION
            # current_site = get_current_site(request)
            # mail_subject = 'Please activate your account'
            # message = render_to_string('accounts/account_verification_email.html', {
            #     'user': user,
            #     'domain': current_site,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': default_token_generator.make_token(user),
            # })
            # to_email = email
            # send_email = EmailMessage(mail_subject, message, to=[to_email])
            # send_email.send()
            # messages.success(request, 'Thank you for registering with us. We have sent you a verification email to your email address [rathan.kumar@gmail.com]. Please verify it.')
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
            login(request, user)

            # request.session['username'] = username
            fname = user.first_name
            messages.success(request, "Logged In Sucessfully!!")
            return redirect('/')
        else:
            messages.error(request, "wrong details!!")
            return redirect('login_user')

    return render(request, "accounts/login.html")


def signout(request):

    logout(request)
    # if 'username' in request.session:
    #     request.session.flush()
    # request.session.flush()

    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')


@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
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


@login_required(login_url='login')
def dashboarduser(request):
    send_message()

    orders = Orders.objects.order_by(
        '-created_at').filter(user_id=request.user.id)
    orders_count = orders.count()

    print(orders_count)
    userprofile = UserProfile.objects.get(user_id=request.user.id)
    context = {
        'orders_count': orders_count,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
def my_orders(request):
    orders = Orders.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'accounts/my_orders.html', context)


@login_required(login_url='login')
def order_detail(request, order_id):

    order = Orders.objects.get(id=order_id)
    # num = order.order_number
    order_detail = OrderProducts.objects.filter(order_number=order.order_number)
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
    
    address = Address.objects.filter(user=request.user)
    
    
    return render(request,'accounts/address.html',{ 'address': address})


def add_address(request):
    if request.method == 'POST':

        adform = AddressForm(request.POST, request.FILES)
        print(adform.errors)
        if adform.is_valid():

            adform.save()

            return redirect('dashboarduser')
        else:
            print('ytuiowetkii')

    adform = AddressForm()
    context = {
        'adform': adform
    }
    return render(request, 'accounts/add_address.html', context)


otp = '0'


def user_otp_sign_in(request):
    '''handle the user otp sign in'''
    print("user otp ethii")
    otp_sign_in_user_status = ''
    if request.method == 'POST':
        print('helloooo')
        phone_number = request.POST.get('phone_number')
        request.session['phone_number'] = phone_number
        print(phone_number)

        if Account.objects.filter(phone_number=phone_number).exists():
            print('heloooo')

            user = Account.objects.get(phone_number=phone_number)
            print(user.email)
            client = Client('SK89ceeec6846fa2465b0fd994cf12dc95',
                                 'e08a6c38c2e9815753a5c3b8fd142442')
            verification = client.verify \
                .v2 \
                .services('MG22325cbe745a8dcd4eced372ea778238') \
                .verifications \
                .create(to='+91{}'.format(phone_number), channel='sms')
            request.session['user'] = user
            user_authentication_status = 'success'
            otp_sign_in_user_status = 'success'
            return JsonResponse({'otp_sign_in_user_status': otp_sign_in_user_status})
        else:
            return render(request, 'accounts/otp_login.html', {'message': "invalid phone number"})
    else:
        return render(request, 'accounts/otp_login.html')

# @never_cache


def user_otp_sign_in_validation(request):
    '''handle the user otp validation'''
    if request.method == 'POST':
        otp_1 = request.POST.get('otp_1')
        otp_2 = request.POST.get('otp_2')
        otp_3 = request.POST.get('otp_3')
        otp_4 = request.POST.get('otp_4')
        # var err = document.getElementById('err')

        user_otp = str(otp_1 + otp_2 + otp_3 + otp_4)
        print(otp)
        print(user_otp)
        contact_number = request.session['user_num']
        client = Client('SK89ceeec6846fa2465b0fd994cf12dc95',
                        'e08a6c38c2e9815753a5c3b8fd142442')
        verification_check = client.verify \
            .v2 \
            .services('MG22325cbe745a8dcd4eced372ea778238') \
            .verification_checks \
            .create(to='+91{}'.format(contact_number), code=user_otp)

        print(verification_check.status)
        user_authentication_status = 'approved'
        # user_authentication_status = 'wrong_otp'
        # if str(user_otp) == str(otp):
        #     user_authentication_status = 'otp_verified'
        #     user = Account.objects.get(contact_number = str(request.session['contact_number']))
        #     request.session['user'] = user.email
        return JsonResponse({'user_authentication_status': user_authentication_status})
    return render(request, 'accounts/otp_login_validation.html')


# def user_otp_sign_in(request):
    
#     phone_number = '7736563119'
#     client = Client('ACe76401d83965afd3d5d67ecb05038e1f',
#                                  'f5ba986fbd2c054c446f74dd299fde5b')
#     verification = client.verify \
#         .v2 \
#          .services('VA45231356f6ed0671efb52f636ae50624') \
#         .verifications \
#         .create(to='+91{}'.format(phone_number), channel='sms')
        
#     return render(request, 'accounts/otp_login.html')

def cancelOrder(request):

    if request.method == 'POST':
        order_id=request.method.POST.get('order_id')
        order = Order.objects.get(id=order_id)
        order.status = 'Cancelled'
        order.save()
    return JsonResponse({'success':'success'})