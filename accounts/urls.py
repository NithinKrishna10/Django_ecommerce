from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login_user/', views.login_user, name='login_user'),
    path('signout/', views.signout, name='signout'),
    path('dashboarduser', views.dashboarduser, name='dashboarduser'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    
    path('my_orders/', views.my_orders, name='my_orders'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('orderproducts/', views.orderproducts, name='orderproducts'),
    path('add_address',views.add_address,name='add_address'),
    path('cancelOrder', views.cancelOrder, name='cancelOrder'),
    path('address_manage',views.address_manage,name='address_manage'),
    path('smslogin/',views.sms_login,name='smslogin'),
    path('otplogin/',views.otp_login,name='otplogin'),
    path('pdf/<pk>',views.invoice_render_pdf_view, name='invoice_pdf_view'),
    path('return_order/<str:order_id>', views.return_order,name='return_order'),

  
]