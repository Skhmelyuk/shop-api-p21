from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path(
        'products/',
        views.ProductListAPIView.as_view(),
        name='product_list'
    ),
    path(
        'product_info/',
         views.ProductInfoAPIView.as_view(),
         name='product_info'
    ),
    path(
        'products/<int:product_id>/',
         views.ProductDetailAPIView.as_view(),
         name='product_detail'
    ),
    path(
        'orders/',
         views.OrderListAPIView.as_view(),
         name='order_list'
    ),
    path(
        'user_orders/',
        views.UserOrderListAPIView.as_view(),
        name='user_order_list'
    ),
]