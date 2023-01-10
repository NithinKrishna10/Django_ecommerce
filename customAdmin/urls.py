from . import views
from django.contrib import admin
from django.urls import  path


urlpatterns = [
    # =================================== admin ===================================
    path('d',views.admin_login,name='admin_login'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('user_management',views.user_management,name='user_management'),
    # path('admin_get_graph_data', views.admin_get_graph_data),
    
    # =================================== product ===================================
    path('product_manage',views.product,name='product_manage'),
    path('add_product',views.add_products,name='add_product'),
    path('edit_product/<str:pk>/', views.edit_product, name='edit_product'),
    path('variations',views.variations,name='variations'),
    path('addVariations',views.addVariations,name='addVariations'),
    path('deleteVariant/<str:pk>/',views.deleteVariant,name='deleteVariant'),
    path('blockVariant/<str:pk>/',views.blockVariant,name='blockVariant'),
    
    # =================================== category ===================================

    path('category',views.category,name='category'),
    path('add_category',views.add_category,name='add_category'),
    path('edit_category/<str:pk>/', views.edit_category, name='edit_category'),
    path('del_category/<str:pk>/', views.del_category, name='del_category'),
    path('brands',views.brands,name='brands'),
    path('addbrand',views.addbrand,name='addbrand'),
    # =================================== user ===================================

    path('adminlogout/', views.adminlogout, name='adminlogout'),
    path('edit_user/<str:pk>/', views.edit_user, name='edit_user'),
    path('block_user/<str:pk>/', views.block_user, name='block_user'),

    # =================================== Order ===================================

    path('orders/', views.orders, name='orders'),
    path('cancelorder/<int:order_id>/', views.cancelorder, name='cancelorder'),
    path('orderdetail/<int:order_id>/', views.orderdetail, name='orderdetail'),
    path('productsorderd/', views.productsorderd, name='productsorderd'),
    path('adminOrderUpdate/<int:order_id>/',views.adminOrderUpdate,name='adminOrderUpdate'),
    path('returnUpdate/<int:order_id>/',views.returnUpdate,name='returnUpdate'),
    
    # =================================== Coupon & Offer ===================================
    path('coupon_mange',views.coupon_mange,name='coupon_mange'),
    path('add_coupon',views.add_coupon,name='add_coupon'),
    path('delete_coupon/<int:coupon_id>/',views.delete_coupon,name='delete_coupon'),
    
    path('offer_category', views.offer_category,name='offer_category'),
    path('delete_offer_category/<int:cat_offer_id>/', views.delete_offer_category,name='delete_offer_category'),
    path('offer_product', views.offer_product,name='offer_product'),
    path('delete_offer_product/<int:pro_offer_id>/', views.delete_offer_product,name='delete_offer_product'),

    
    
    # ==================================== Sales Report ======================================
    path('sales',views.sales_report_date, name='sales'),
    path('export_to_pdf',views.export_to_pdf, name='export_to_pdf'),
    path('export_to_excel',views.export_to_excel, name='export_to_excel'),
    
]

