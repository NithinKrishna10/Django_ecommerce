from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from accounts.models import Account
from orders.models import Order, OrderProduct
from .forms import CategoryForm, ProductForm, UserForm, VariationsForm,BrandForm
from store.models import Product, Category, Variation,Brand
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
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

            if user_obj.is_superadmin and user_obj:
                login(request, user_obj)
                return redirect('dashboard/')
                # return render(request,'admin/index.html' )

            messages.info(request, 'Invalid Password')
            return render('customadmin/adminlogin.html')
        return render(request, 'customadmin/adminlogin.html')

    except Exception as e:
        print('e')
    return render(request, 'customadmin/adminlogin.html')


def dashboard(request):
    if request.user.is_authenticated:
        
        orderitem = OrderProduct.objects.all()
        labels = []
        data = []
        
        queryset = OrderProduct.objects.order_by('quantity')[:5]
        for city in queryset:
            labels.append(city.product)
            data.append(city.quantity)
      
        context = {
            'orderitem' : orderitem,
            'labels' : labels,
            'data' : data
        }

        return render(request, 'customadmin/dashboard.html',context)

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

        bform = BrandForm(request.POST or None, request.FILES or None)
 
        if bform.is_valid():

            bform.save()

            return JsonResponse({'message': 'works'})
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
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'customadmin/ordermanage.html', context)

@login_required(login_url='login')
def cancelorder(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        order.status = 'Cancelled'
        order.save()

    return redirect('orders')


def orderdetail(request, order_id):

    order = Order.objects.get(id=order_id)
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
