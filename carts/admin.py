# Core django imports
from django.contrib import admin

# Local imports
from .models import Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("__str__", "product", "quantity", "id")
    search_fields = ("product",)
