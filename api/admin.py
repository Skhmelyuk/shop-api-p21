from django.contrib import admin
from .models import User, Product, Order, OrderItem

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    list_filter = ['is_staff', 'is_superuser', 'is_active']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id",'name', 'price', 'stock', 'is_in_stock']
    list_filter = ['stock']
    search_fields = ['name', 'description']
    readonly_fields = ['is_in_stock']


class OrderItemInline(admin.TabularInline):
    """
    Inline для відображення OrderItem в Order.
    """
    model = OrderItem
    extra = 1
    readonly_fields = ['total_price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Адмін панель для моделі Order.
    """
    list_display = ['order_id', 'user', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order_id', 'user__username']
    readonly_fields = ['order_id', 'created_at']
    list_editable = ['status']
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """
    Адмін панель для моделі OrderItem.
    """
    list_display = ['order', 'product', 'quantity', 'total_price']
    list_filter = ['order__status']
    readonly_fields = ['total_price']
