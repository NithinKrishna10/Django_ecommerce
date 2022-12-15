from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login_user/', views.login_user, name='login_user'),
    path('signout/', views.signout, name='signout'),
    path('dashboarduser', views.dashboarduser, name='dashboarduser'),
    
    
    path('my_orders/', views.my_orders, name='my_orders'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
]