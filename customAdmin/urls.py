from . import views
from django.contrib import admin
from django.urls import  path


urlpatterns = [
    # =================================== admin ===================================
    path('d',views.admin_login,name='admin_login'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('user_management',views.user_management,name='user_management'),
    
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
    # =================================== user ===================================

    path('adminlogout/', views.adminlogout, name='adminlogout'),
    path('edit_user/<str:pk>/', views.edit_user, name='edit_user'),
    path('block_user/<str:pk>/', views.block_user, name='block_user'),
]