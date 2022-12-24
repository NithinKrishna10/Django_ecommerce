
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, render, redirect
from orders.models import OrderProduct

from orders.models import Order,Orders
from .models import Account, UserProfile

# from accounts.forms import UserAdminCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegistrationForm, UserForm, UserProfileForm
from django.contrib.sites.shortcuts import get_current_site
from .mixins import send_otp_on_phone




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
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
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
    # send_otp_on_phone()
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
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
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




@login_required(login_url = 'login')
def dashboarduser(request):
    orders = Orders.objects.order_by('-created_at').filter(user_id=request.user.id)
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
    order_detail = OrderProduct.objects.filter(order_number=order.order_number)
    subtotal = 0
    
    
    
    for i in order_detail:
        subtotal += i.product_price * i.quantity
 
    
    
    # orderdetail = OrderProduct.objects.filter(order=order_id)
    # # orderdetail = OrderProduct.objects.get(order=order_id)
    # order = Order.objects.get(pk=order_id)
    
    
    
    # for i in orderdetail:
    #     subtotal += i.product_price * i.quantity
    # print(subtotal)
    context = {
        'order_detail': order_detail,
        'order': order,
        'subtotal': subtotal,
    }
    return render(request, 'accounts/order_detail.html', context)


# def order_detail(request, order_id):
#     order = Order.objects.get(order_number = order_id)
#     order_detail = OrderProduct.objects.filter(order__order_number=order_id)
#     order_detail.
#     subtotal = 0
    
#     for i in order_detail:
#         subtotal += i.product_price * i.quantity

#     context = {
#         'order_detail': order_detail,
#         'order': order,
#         'subtotal': subtotal,
#     }
#     return render(request, 'accounts/order_detail.html', context)


@login_required(login_url='login')
def cancel_order(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        order.status = 'Cancelled'
        order.save()


    return redirect('my_orders')


@login_required(login_url='login')
def orderproducts(request):
    
    orderitems = OrderProduct.objects.all()
    orders = Orders.objects.filter(user=request.user)
    
    context = {
        'orderitems' : orderitems,
        'orders' : orders,
    }
    
    return render(request , 'accounts/orderproducts.html',context)
