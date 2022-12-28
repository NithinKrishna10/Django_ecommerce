from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from accounts.models import Account
from orders.models import Order, OrderProduct,Orders
from .forms import CategoryForm, ProductForm, UserForm, VariationsForm,BrandForm
from store.models import Product, Category, Variation,Brand
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
import datetime
from datetime import date, timedelta

# Create your views here.


# ========================================== Admin Login Function ========================================== #


def admin_login(request):
    try:
        if request.user.is_authenticated:
            return redirect('dashboard/')

        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']

            user_obj = Account.objects.filter(email=email)
            if not user_obj.exists():
                messages.info(request, 'Account not found')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            user_obj = auth.authenticate(email=email, password=password)

            if user_obj.is_admin and user_obj:
                login(request, user_obj)
                return redirect('dashboard/')
                # return render(request,'admin/index.html' )

            messages.info(request, 'Invalid Password')
            return render('customadmin/adminlogin.html')
        return render(request, 'customadmin/adminlogin.html')

    except Exception as e:
        print('e')
    return render(request, 'customadmin/adminlogin.html')





   
def dasshboard(request):
    if request.user.is_authenticated:
        
        orderitem = OrderProduct.objects.all()
        labels = []
        data = []
        
        queryset = OrderProduct.objects.order_by('quantity')
        for city in queryset:
            labels.append(city.product)
            data.append(city.quantity)
        #     sales = Orders.objects.filter(status='Delivered')
        #     revenue = 0
        #     for sale in sales:
        #          revenue = revenue + sale.order_total
        
        # this_admin = Account.objects.get(email=admin_email)
        user_count = Account.objects.all().count()
        sales = Orders.objects.filter(status='Placed')
        revenue = 0
        for sale in sales:
            revenue = revenue + sale.order_total
        context = {
            'data':data,
            'labels' : labels,
            'revenue' : revenue,
            'duration': '',
            'sales': sales.count,
            'customer_count': user_count,
            
        }

        return render(request, 'customadmin/admin_panel.html',context)

    else:
        return redirect('admin_login')


def user_management(request):

    if request.user.is_authenticated:
        
        user_det = Account.objects.all()
        
        return render(request, 'customadmin/user.html', {'user_det': user_det})

    else:
        return redirect('admin_login')


def edit_user(request, pk):
    user = Account.objects.get(id=pk)
    uform = UserForm(instance=user)

    if request.method == 'POST':
        uform = UserForm(request.POST, instance=user)
        if uform.is_valid():
            uform.save()
        return redirect('user_management')

    context = {
        'uform': uform
    }
    return render(request, 'customadmin/useredit.html', context)


def block_user(request, pk):
    user = Account.objects.get(id=pk)
    if request.method == 'POST':

        if user.is_active == True:

            user.is_active = False
            user.save()
        else:
            user.is_active = True
            user.save()

        return redirect('user_management')


# ========================================== Admin Product Functions ========================================== #


def product(request):
    if request.user.is_authenticated:

        products = Product.objects.all()

        return render(request, 'customadmin/productmanage.html', {'products': products})
    else:
        return redirect('admin_login')


def add_products(request):
    print('hoii')
    if request.method == 'POST':

        pform = ProductForm(request.POST, request.FILES)
 
        if pform.is_valid():

            pform.save()

            return redirect('product_manage')
        else:
            print('ytuiowetkii')

    pform = ProductForm()
    context = {
        'pform': pform
    }
    return render(request, 'customadmin/addproduct.html', context)


def edit_product(request, pk):
    product = Product.objects.get(id=pk)
    pform = ProductForm(instance=product)

    if request.method == 'POST':
        pform = ProductForm(request.POST, instance=product)

        if pform.is_valid():
            pform.save()
        return redirect('product_manage')

    context = {
        'pform': pform
    }
    return render(request, 'customadmin/editproduct.html', context)


def variations(request):

    productv = Variation.objects.all()

    context = {

        'productv': productv,
    }

    return render(request, 'customadmin/productvariant.html', context)


def addVariations(request):

    if request.user.is_authenticated:
        if request.method == 'POST':
            vaform = VariationsForm(request.POST)

            print(vaform.errors)
            if vaform.is_valid():
                vaform.save()
            return redirect('variations')
        vaform = VariationsForm()
        context = {
            'vaform': vaform
        }
        return render(request, 'customadmin/addvariant.html', context)
    else:
        return redirect('variations')


def blockVariant(request, pk):
    variant = Variation.objects.get(id=pk)
    if request.method == 'POST':

        if variant.is_active == True:

            variant.is_active = False
            variant.save()
        else:
            variant.is_active = True
            variant.save()

        return redirect('variations')


def deleteVariant(request, pk):

    variants = Variation.objects.get(id=pk)
    if request.method == 'POST':
        variants.delete()

        return redirect('variations')

def brands(request):
    brand = Brand.objects.all()
    
    return render(request,'customadmin/brand.html',{ 'brand':brand })
def addbrand(request):

    if request.method == 'POST':

        bform = BrandForm(request.POST ,request.FILES )
        print(bform.errors)
        if bform.is_valid():

            bform.save()

            # return JsonResponse({'message': 'works'})
            return redirect('brands')
            
        else:
            print('ytuiowetkii')

    bform = BrandForm()
    
    context = {
        'bform': bform
    }
 
    return render(request, 'customadmin/addbrand.html',context)

# ========================================== Admin Category Functions ========================================== #

def category(request):

    category = Category.objects.all()

    return render(request, 'customadmin/category.html', {'category': category})


def add_category(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            cform = CategoryForm(request.POST, request.FILES)

            print(cform.errors)
            if cform.is_valid():
                cform.save()
            return redirect('category')
        cform = CategoryForm()
        context = {
            'cform': cform
        }
        return render(request, 'customadmin/addcategory.html', context)
    else:
        return redirect('admin_login')


def edit_category(request, pk):
    cate = Category.objects.get(id=pk)
    cform = CategoryForm(instance=cate)

    if request.method == 'POST':
        cform = CategoryForm(request.POST, instance=cate)
        if cform.is_valid():
            cform.save()
        return redirect('category')

    context = {
        'cform': cform
    }
    return render(request, 'customadmin/editcategory.html', context)


def del_category(request, pk):

    cate = Category.objects.get(id=pk)
    if request.method == 'POST':
        cate.delete()

        return redirect('category')


def adminlogout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('admin_login')


# ======================== Orders ============================



@login_required(login_url='login')
def orders(request):
    orders = Orders.objects.all().order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'customadmin/ordermanage.html', context)

@login_required(login_url='login')
def cancelorder(request, order_id):
    order = Orders.objects.get(id=order_id)
    if request.method == 'POST':
        order.status = 'Cancelled'
        order.save()

    return redirect('orders')


def orderdetail(request, order_id):

    order = Orders.objects.get(id=order_id)
    # num = order.order_number
    orderdetail = OrderProduct.objects.filter(order_number=order.order_number)
    subtotal = 0

    for i in orderdetail:
        subtotal += i.product_price * i.quantity

    context = {
        'orderdetail': orderdetail,
        'order': order,
        'subtotal': subtotal,
    }
    return render(request, 'customadmin/aorderdetail.html', context)


@login_required(login_url='login')
def productsorderd(request):

    orderitems = OrderProduct.objects.all()
    # orders = Order.objects.filter(user=request.user)

    context = {
        'orderitems': orderitems,
        # 'orders' : orders,
    }

    return render(request, 'customadmin/orderd_products.html', context)


def adminOrderUpdate(request, order_id):
    order = Orders.objects.get(id=order_id)
    if request.method == 'POST':
        order = Orders.objects.get(id=order_id)
        print(order.status)
        if order.status == 'Accepted':
            order.status = 'Placed'
            order.save()
            print(order.status)
        elif order.status == 'Placed':
            order.status = 'Shipped'
            print(order.status)
            order.save()
            # return redirect('orders')
        elif order.status == 'Shipped':
            print(order.status)
            order.status = 'Out For Delivery'
            order.save()
            # return redirect('orders')
        elif order.status == 'Out For Delivery':
            print(order.status)
            order.status = 'Delivered'
            order.save()
            # return redirect('orders')
        else:
            order.status = 'Delivered'
            order.save()
            # return redirect('orders')
        
    return redirect('orders')
    # return render(request, 'admin_order_details.html',
    #               {'order': order, 'address': address, 'next_status': next_status, 'admin': this_admin})






# =============================================================================


current_date = datetime.date.today()
duration = 'Today'

def dashboard(request):
    admin = ''
    # if 'admin' in request.session:
    #     admin = request.session['admin']
    # else:
    #     return redirect('/admin_sign_in')
    # this_admin = Account.objects.get(email=admin)
    sales_graph_data = []
    sales_graph_category = []
    user_graph_data = []
    user_graph_category = []
    if request.method == 'POST':
        duration = request.POST.get('duration')
        print('Getting Graph details of ', duration)
        orders = Orders.objects.all()
        users = Account.objects.all()
        if duration == 'today':
            sales_graph_data = []
            sales_graph_category = []
            user_graph_data = []
            user_graph_category = []
            count = 0
            # finding the number of sales on today based on orders
            cycle = 0
            for sale in orders:
                cycle = cycle + 1
                # filtering sales based on year
                if str(sale.Order_year) == str(current_date.year):
                    # filtering sales based on month
                    if str(sale.Order_month) == str(current_date.month):
                        # filtering sales based on day
                        if str(sale.Order_day) == str(current_date.day):
                            # filterin sales which has the status as delivered based on orders
                            print(sale.status)
                            if str(sale.status == 'delivered'):
                                count = count + 1
                            sales_graph_data.append(count)
                            sales_graph_category.append(cycle)
            # printing the number of sales on today
            print('Number of sales In Today Is ', count)
            for user in users:
                # filtering sales based on year
                if str(user.signup_year) == str(current_date.year):
                    # filtering sales based on month
                    if str(user.signup_month) == str(current_date.month):
                        # filtering sales based on day
                        if str(user.signup_day) == str(current_date.day):
                            count = count + 1
                            user_graph_data.append(4)
                            user_graph_category.append(1)
        elif duration == 'last_7_days':
            sales_graph_data = []
            sales_graph_category = []
            user_graph_data = []
            user_graph_category = []
            count = 0
            # getting the sales of last  days
            # value of day is from 1 to 7
            for day in range(0, 7):
                count = 0
                for sale in orders:
                    if str(sale.Order_year) == str(current_date.year):
                        # print(sale.Order_day,current_date.day-timedelta(days=day).days)
                        if str(sale.Order_day) == str(current_date.day - (timedelta(days=day).days)):
                            # print('count+',count)
                            count = count + 1
                sales_graph_data.append(count)
                sales_graph_category.append(current_date.day - (timedelta(days=day).days))
            print('Number of sales in the last 7 days is ', sales_graph_data)
            # getting the new users
            for day in range(0, 7):
                count = 0
                for user in users:
                    if str(user.signup_year) == str(current_date.year):
                        if str(user.signup_month) == str(current_date.month):
                            # print(sale.Order_day,current_date.day-timedelta(days=day).days)
                            if str(user.signup_day) == str(current_date.day - (timedelta(days=day).days)):
                                # print('count+',count)
                                count = count + 1
                user_graph_data.append(count)
                user_graph_category.append(current_date.day - (timedelta(days=day).days))
            print('Number of revenue in the last 7 days is ', user_graph_data)
        # this month
        elif duration == 'last_month':
            sales_graph_data = []
            sales_graph_category = []
            user_graph_data = []
            user_graph_category = []
            count = 0
            for day in range(1, 32):
                count = 0
                for sale in orders:
                    if str(sale.Order_year) == str(current_date.year):
                        if str(sale.Order_month) == str(current_date.month):
                            if str(sale.Order_day) == str(day):
                                count = count + 1
                sales_graph_data.append(count)
                sales_graph_category.append(day)
            for day in range(1, 32):
                count = 0
                for user in users:
                    if str(user.signup_year) == str(current_date.year):
                        if str(user.signup_month) == str(current_date.month):
                            if str(user.signup_day) == str(day):
                                count = count + 1
                user_graph_data.append(count)
                user_graph_category.append(day)
        # this year
        else:
            sales_graph_data = []
            sales_graph_category = []
            user_graph_data = []
            user_graph_category = []
            count = 0
            for month in range(1, 13):
                count = 0
                for sale in orders:
                    if str(sale.Order_year) == str(current_date.year):
                        if str(sale.Order_month) == str(month):
                            count = count + 1
                sales_graph_data.append(count)
                sales_graph_category.append(month)
            for month in range(1, 13):
                count = 0
                for user in users:
                    if str(user.signup_year) == str(current_date.year):
                        if str(user.signup_month) == str(month):
                            count = count + 1
                user_graph_data.append(count)
                user_graph_category.append(month)
    user_count = Account.objects.all().count()
    sales = Orders.objects.filter(status='Delivered')
    cod = Orders.objects.filter(payment_mode='Cash on Delivery').count()
    paypal = Orders.objects.filter(payment_mode='paypal').count()
    razorpay = Orders.objects.filter(payment_mode='Paid by Razorpay').count()
    paypal_payment_method_graph_data = paypal
    razorpay_payment_method_graph_data = razorpay
    cod_payment_method_graph_data = cod
    revenue = 0
    for sale in sales:
        revenue = revenue + sale.order_total
    return render(request, 'customadmin/admin_panel.html', {
        # 'duration': duration,
        'customer_count': user_count,
        'sales': sales.count(),
        'revenue': revenue,
        # 'admin': this_admin,
        'sales_graph_data': sales_graph_data,
        'sales_graph_category': sales_graph_category,
        'user_graph_data': user_graph_data,
        'user_graph_category': [user_graph_category],
        'paypal_payment_method_graph_data': paypal_payment_method_graph_data,
        'razorpay_payment_method_graph_data': razorpay_payment_method_graph_data,
        'cod_payment_method_graph_data': cod_payment_method_graph_data,
    })
    
    
