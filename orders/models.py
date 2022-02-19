# Core django imports
from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth import get_user_model
from django.conf import settings

# Local imports
from products.models import Product

User = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    discount = models.PositiveIntegerField(
        validators=[MaxValueValidator(100)], null=True, blank=True
    )

    def __str__(self):
        return f"{self.user}"

    @property
    def get_total_price(self):
        total = sum(i.price() for i in self.order_item.all())
        if self.discount:
            discount_price = (self.discount * total) / 100
            return int(total - discount_price)
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    order = models.ForeignKey(
        Order, on_delete=models.PROTECT, related_name="order_item"
    )
    quantity = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"{self.product.title} - {self.order}"
