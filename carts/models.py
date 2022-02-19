# Stdlib imports
from uuid import uuid4

# Core django imports
from django.db import models
from django.contrib.auth import get_user_model

# Local imports
from products.models import Product

User = get_user_model()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.user.username}"
