from rest_framework import serializers
from .models import User, Product, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name', 
            'description', 
            'price', 
            'stock'
        ]


    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative")
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer для моделі OrderItem"""

    # product = ProductSerializer(read_only=True)
    product_name = serializers.CharField(
        source='product.name',
        max_length=100,
        read_only=True
    )
    product_price = serializers.DecimalField(
        source='product.price',
        max_digits=10, 
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = OrderItem
        fields = [
            'product_name', 
            'product_price', 
            'quantity', 
            'total_price'
        ]


class OrderSerializer(serializers.ModelSerializer):
    """Serializer для моделі Order"""

    items = OrderItemSerializer(many=True, read_only=True)

    total_order = serializers.SerializerMethodField(method_name='total')

    def total(self, obj):
        order_items = obj.items.all()
        total = sum(item.total_price for item in order_items)
        return total
    
    class Meta:
        model = Order
        fields = [
            'order_id',
            'created_at',
            'user', 
            'status', 
            'items', 
            'total_order'
        ]

class ProductInfoSerializer(serializers.Serializer):
    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()