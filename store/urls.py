from . import views
from django.contrib import admin
from django.urls import  path


urlpatterns = [
    #   path('productview/<int:id>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    # path('product_detail/<str:product_slug>',views.product_detail,name='product_detail'),
      path('store_view/',views.store_view,name='store_view'),
      path('product_details/<slug:category_slug>/<slug:product_slug>/<int:product_id>', views.product_detail, name='product_detail'),

]