from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse


from django.template.loader import *
from django.db.models import Count,Sum
from .models import SalesReport,sales_report,monthly_sales_report,Categoryoffer,Productoffer
from accounts.models import Account,Return_request
from orders.models import Order, OrderProducts,Orders
from .forms import  ProductForm, UserForm, VariationsForm,BrandForm,CategoryOfferForm,CategoryForm,CouponForm,ProductOfferForm
from store.models import Product, Category, Variation,Brand
from cart.models import Coupon
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
import datetime
from datetime import date, timedelta
import io
from xhtml2pdf import pisa 
import xlwt
from django.http import FileResponse


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





@login_required(login_url='admin_login') 
def dasshboard(request):
    if request.user.is_authenticated:
        
        orderitem = OrderProducts.objects.all()
        labels = []
        data = []
        
        queryset = OrderProducts.objects.order_by('quantity')
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

@login_required(login_url='admin_login')
def user_management(request):

    if request.user.is_authenticated:
        
        user_det = Account.objects.all()
        
        return render(request, 'customadmin/user.html', {'user_det': user_det})

    else:
        return redirect('admin_login')

@login_required(login_url='admin_login')
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

@login_required(login_url='admin_login')
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

@login_required(login_url='admin_login')
def product(request):
    if request.user.is_authenticated:

        products = Product.objects.all()

        return render(request, 'customadmin/productmanage.html', {'products': products})
    else:
        return redirect('admin_login')

@login_required(login_url='admin_login')
def add_products(request):
    print('hoii')
    
    if request.method == 'POST':

        pform = ProductForm(request.POST, request.FILES)
        print(pform.errors)
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

@login_required(login_url='admin_login')
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

@login_required(login_url='admin_login')
def variations(request):

    productv = Variation.objects.all()

    context = {

        'productv': productv,
    }

    return render(request, 'customadmin/productvariant.html', context)

@login_required(login_url='admin_login')
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

@login_required(login_url='admin_login')
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

@login_required(login_url='admin_login')
def deleteVariant(request, pk):

    variants = Variation.objects.get(id=pk)
    if request.method == 'POST':
        variants.delete()

        return redirect('variations')
    
@login_required(login_url='admin_login')
def brands(request):
    brand = Brand.objects.all()
    
    return render(request,'customadmin/brand.html',{ 'brand':brand })

@login_required(login_url='admin_login')
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
@login_required(login_url='admin_login')
def category(request):

    category = Category.objects.all()

    return render(request, 'customadmin/category.html', {'category': category})

@login_required(login_url='admin_login')
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

@login_required(login_url='admin_login')
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

@login_required(login_url='admin_login')
def del_category(request, pk):

    cate = Category.objects.get(id=pk)
    if request.method == 'POST':
        cate.delete()

        return redirect('category')

@login_required(login_url='admin_login')
def adminlogout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('admin_login')


# ======================== Orders ============================



@login_required(login_url='admin_login')
def orders(request):
    orders = Orders.objects.all().order_by('-created_at')
    return_order = Return_request.objects.all()
    context = {
        'orders': orders,
        'return_order' : return_order
    }
    return render(request, 'customadmin/ordermanage.html', context)

@login_required(login_url='admin_login')
def cancelorder(request, order_id):
    order = Orders.objects.get(id=order_id)
    if request.method == 'POST':
        order.status = 'Cancelled'
        order.save()

    return redirect('orders')

@login_required(login_url='admin_login')
def returnUpdate(request, order_id):
    order = Orders.objects.get(id=order_id)
    if request.method == 'POST':
        order.status = 'Return Accepted'
        order.save()

    return redirect('orders')


@login_required(login_url='admin_login')
def orderdetail(request, order_id):

    order = Orders.objects.get(id=order_id)
    # num = order.order_number
    orderdetail = OrderProducts.objects.filter(order_number=order.order_number)
    subtotal = 0

    for i in orderdetail:
        subtotal += i.product_price * i.quantity

    context = {
        'orderdetail': orderdetail,
        'order': order,
        'subtotal': subtotal,
    }
    return render(request, 'customadmin/aorderdetail.html', context)

@login_required(login_url='admin_login')
def productsorderd(request):

    orderitems = OrderProducts.objects.all()
    # orders = Order.objects.filter(user=request.user)

    context = {
        'orderitems': orderitems,
        # 'orders' : orders,
    }

    return render(request, 'customadmin/orderd_products.html', context)


@login_required(login_url='admin_login')
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
@login_required(login_url='admin_login')
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



    
# ========================== Coupon ==========================
@login_required(login_url='admin_login')
def coupon_mange(request):
    
    coupon = Coupon.objects.all()
    messages.success(request , 'Deleted Sucssful')   
    return render(request,'customadmin/coupenManage.html',{'coupon': coupon})


@login_required(login_url='admin_login')
def add_coupon(request):
    
    if request.user.is_authenticated:
        if request.method == 'POST':
            cnform = CouponForm(request.POST, request.FILES)

            print(cnform.errors)
            if cnform.is_valid():
                cnform.save()
            return redirect('coupon_mange')
        cnform = CouponForm()
        context = {
            'cnform': cnform
        }
        return render(request, 'customadmin/add_coupon.html', context)
    else:
        return redirect('admin_login')


def delete_coupon(request,coupon_id):
    coupon = Coupon.objects.get(id = coupon_id)
    coupon.delete()
    
    return redirect('coupon_mange')
    
# ========================== Offers ==========================

def offer_product(request):
    pro = Product.objects.all()
    pro_offer = Productoffer.objects.all()
    poform = ProductOfferForm()
    if request.method=='POST':
        discount=int(request.POST.get('discount'))
        product =request.POST.get('product')
        is_active=request.POST.get('is_active')
        if Productoffer.objects.filter(product=product).exists():
            print('is exists')
            messages.success(request , 'Offer is exists')
        else:
            print('no')
            Productoffer.objects.create(product=product,discount=discount,is_active=is_active)
            product = Product.objects.get(product_name=product)
            print(product.product_name)
            if product.offer_percentage < discount:
                print('hai offer')
                price=float(product.original_price)
                product.price = price-price*float(discount)/100
                product.offer_percentage = discount
                product.save()
                messages.success(request , 'Offer is Applied')
                
            else:
                pass
            
        
        return redirect('offer_product')
    
    context={
            'pro' : pro,
            'pro_offer': pro_offer, 
             'poform':poform,
             }
    return render(request,'customadmin/product_offer.html',context)   
    
def delete_offer_product(request,pro_offer_id):
    productoff = Productoffer.objects.get(id = pro_offer_id)
    product=Product.objects.get(product_name=productoff.product )
    
    
    if Categoryoffer.objects.filter(category=product.category).exists():
        catoff = Categoryoffer.objects.get(category=product.category)
        discount = catoff.discount
        price=float(product.original_price)
        product.price=price-price*float(discount)/100
        product.offer_percentage = discount
        product.save()
        messages.success(request , 'Offer is deleted')
    else:
        product.price = product.original_price
        product.offer_percentage = 0
        product.save()    
        messages.success(request , 'Offer is Deleted')
    productoff.delete()
    
    return redirect('offer_category')
    



def offer_category(request):
    cat = Category.objects.all()
    cat_offer = Categoryoffer.objects.all()
    coform = CategoryOfferForm()
    
    if request.method=='POST':
        discount=int(request.POST.get('discount'))
        category=request.POST.get('category')
        is_active=request.POST.get('is_active')
        print(category)
        if Categoryoffer.objects.filter(category=category).exists():
            print('is exists')
            messages.success(request , 'Offer is exists')
        else:
            print('no')
            Categoryoffer.objects.create(category=category,discount=discount,is_active=is_active)
            cat=Category.objects.get(category_name=category).pk
            product=Product.objects.filter(category=cat)
            
            for items in product:
                print(type(items.offer_percentage))
                print(type(discount))
                if items.offer_percentage < discount:
                    print(items.product_name)
                    price=float(items.original_price)
                    items.price=price-price*float(discount)/100
                    items.offer_percentage = discount
                    items.save()
            messages.success(request , 'Offer Added Sucssfully')   
            return redirect('offer_category')
    context ={
        'cat_offer': cat_offer,
        'coform':coform,
        'cat':cat,
        }
    return render(request,'customadmin/category_offer.html',context)   



def delete_offer_category(request,cat_offer_id):
    categoryoff = Categoryoffer.objects.get(id = cat_offer_id)
    cat=Category.objects.get(category_name=categoryoff.category )
    product=Product.objects.filter(category=cat)
    discount = categoryoff.discount
    for items in product:
        if Productoffer.objects.filter(product=items.product_name).exists():
            poff =Productoffer.objects.get(product=items.product_name)
            discount = poff.discount
            print(items.product_name)
            products = Product.objects.get(product_name=items.product_name)
            price=float(products.original_price)
            products.price = price-price*float(discount)/100
            products.offer_percentage = discount
            print(products.offer_percentage)
            products.save()
        else:
               
            print(items.product_name)
            items.price=items.original_price
            items.offer_percentage = 0
            items.save()
    categoryoff.delete()
    
    return redirect('offer_category')
    


# ===================================== Sales Report =================================

@login_required(login_url='admin_login')
def sales_report_date(request):
    data = OrderProducts.objects.all()
    if request.method == 'POST':
        if request.POST.get('month'):
            month = request.POST.get('month')
            print(month)
            data = OrderProducts.objects.filter(created_at__icontains=month)
            
            if data:
                if SalesReport.objects.all():
                    SalesReport.objects.all().delete()
                    for i in data:
                        sales = SalesReport()
                        sales.productName = i.product.product_name
                        sales.categoryName = i.product.category.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'customadmin/sales_report_.html',context)
                else:
                    for i in data:
                        sales = SalesReport()
                        sales.productName = i.product.product_name
                        sales.categoryName = i.product.category.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'customadmin/sales_report_.html',context)
            else:
                messages.warning(request,"Nothing Found!!")
        if request.POST.get('date'):
            date = request.POST.get('date')
            print("0,",date)
            
            date_check = OrderProducts.objects.filter(created_at__icontains=date)
            print(date_check)
            if date_check:
                if SalesReport.objects.all():
                    SalesReport.objects.all().delete()
            
                    for i in date_check:
                        sales = SalesReport()
                        sales.productName = i.product.product_name
                        sales.categoryName = i.product.category.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'customadmin/sales_report_.html',context)
                else:
                    for i in date_check:
                        sales = SalesReport()
                        sales.productName = i.product.product_name
                        sales.categoryName = i.product.category.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'customadmin/sales_report_.html',context)
            else:
                messages.warning(request,"Nothing Found!!")
        if request.POST.get('date1'):
            date1 = request.POST.get('date1')
            date2 = request.POST.get('date2')
            data_range = OrderProducts.objects.filter(created_at__gte=date1,created_at__lte=date2)
            if data_range:
                if SalesReport.objects.all():
                    SalesReport.objects.all().delete()
            
                    for i in data_range:
                        sales = SalesReport()
                        sales.productName = i.product.product_name
                        sales.categoryName = i.product.category.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'customadmin/sales_report_.html',context)
                else:
                    for i in data_range:
                        sales = SalesReport()
                        sales.productName = i.product.product_name
                        sales.categoryName = i.product.category.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'customadmin/sales_report_.html',context)
            else:
                messages.warning(request,"Nothing Found!!")
    if data:
        if SalesReport.objects.all():
            SalesReport.objects.all().delete()
            for i in data:
                sales = SalesReport()
                sales.productName = i.product.product_name
                sales.categoryName = i.product.category.category_name
                sales.date = i.created_at
                sales.quantity = i.quantity
                sales.productPrice = i.product_price
                sales.save()
            sales = SalesReport.objects.all()
            total = SalesReport.objects.all().aggregate(Sum('productPrice'))
            context = { 'sales':sales,'total':total['productPrice__sum']}
            return render(request,'customadmin/sales_report_.html',context)

        else:
            for i in data:
                sales = SalesReport()
                sales.productName = i.product.product_name
                sales.categoryName = i.product.category.category_name
                sales.date = i.created_at
                sales.quantity = i.quantity
                sales.productPrice = i.product_price
                sales.save()
            sales = SalesReport.objects.all()
            total = SalesReport.objects.all().aggregate(Sum('productPrice'))
            context = { 'sales':sales,'total':total['productPrice__sum']}
            return render(request,'customadmin/sales_report_.html',context)
        
    else:
        messages.warning(request,"Nothing Found!!")
    
    return render(request,'customadmin/sales_report_.html')


@login_required(login_url='admin_login')
def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return

@login_required(login_url='admin_login')
def export_to_excel(request):
    response = HttpResponse(content_type = 'application/ms-excel')
    response['content-Disposition'] = 'attachment; filename="sales.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sales Report') #this will generate a file named as sales Report

     # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Product Name','Category','Price','Quantity', ]

    for col_num in range(len(columns)):
        # at 0 row 0 column
        ws.write(row_num, col_num, columns[col_num], font_style)

    
    font_style = xlwt.XFStyle()
    total = 0

    rows = SalesReport.objects.values_list(
        'productName','categoryName', 'productPrice', 'quantity')
    for row in rows:
        total +=row[2]
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    row_num += 1
    col_num +=1
    ws.write(row_num,col_num,total,font_style)

    wb.save(response)

    return response

# @never_cache
@login_required(login_url='admin_login')
def export_to_pdf(request):
    prod = Product.objects.all()
    order_count = []
    # for i in prod:
    #     count = SalesReport.objects.filter(product_id=i.id).count()
    #     order_count.append(count)
    #     total_sales = i.price*count
    sales = SalesReport.objects.all()
    total_sales = SalesReport.objects.all().aggregate(Sum('productPrice'))



    template_path = 'customadmin/sales_pdf.html'
    context = {
        'brand_name':prod,
        'order_count':sales,
        'total_amount':total_sales['productPrice__sum'],
    }
    
    # csv file can also be generated using content_type='application/csv
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response



