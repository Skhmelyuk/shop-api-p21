from re import search
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer
from rest_framework.decorators import api_view
from django.db.models import Max
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from .pagination import ProductPagination, OrderPagination

class ProductListAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all().order_by('pk')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'stock']
    pagination_class = PageNumberPagination
    pagination_class.page_size = 2
    
    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    lookup_url_kwarg = 'product_id'


class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product').order_by('pk')
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [SearchFilter]
    search_fields = ['user__username']
    pagination_class = OrderPagination


class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        return qs.filter(user=user)


class ProductInfoAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({
            'products': products,
            'count': products.count(),
            'max_price': products.aggregate(max_price=Max('price'))['max_price']
        })
        return Response(serializer.data)


# @api_view(['GET'])
# def product_info(request):
#     products = Product.objects.all()
    
#     serializer = ProductInfoSerializer({
#         'products': products,
#         'count': products.count(),
#         'max_price': products.aggregate(max_price=Max('price'))['max_price']
#     })
    
#     return Response(serializer.data)