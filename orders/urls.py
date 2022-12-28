from django.urls import path
from . import views



urlpatterns = [
    path('place_order', views.place_order, name='place_order'),
    path('order_place', views.order_place, name='order_place'),
    path('proceed-to-pay',views.razorpaycheck,name='razorpaycheck'),
    # path('payments/', views.payments, name='payments'),
    path('order_complete/', views.order_complete, name='order_complete'),
    path('orsu/', views.orsu, name='orsu'),
]
