from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    pass
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    stock = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

    @property
    def is_in_stock(self):
        return self.stock > 0


class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'pending',
        COMPLETED = 'completed',
        CANCELLED = 'cancelled',

    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    product = models.ManyToManyField(Product, through='OrderItem')
    
    def __str__(self):
        return f"{self.product.name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.product.name}"

    @property
    def total_price(self):
        return self.product.price * self.quantity
