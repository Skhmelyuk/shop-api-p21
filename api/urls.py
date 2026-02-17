
from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('product_info/', views.product_info, name='product_info'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('orders/', views.order_list, name='order_list'),
]