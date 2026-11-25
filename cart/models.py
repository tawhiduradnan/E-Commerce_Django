from django.conf import settings
from django.db import models


class Cart(models.Model):
    customer = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart",
    )

    def __str__(self):
        return f"Cart for {self.customer}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    variant = models.ForeignKey(
        "products.ProductVariant",
        on_delete=models.CASCADE,
        related_name="cart_items",
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("cart", "variant"), name="unique_variant_per_cart"
            ),
            models.CheckConstraint(
                condition=models.Q(quantity__gte=1), name="cart_item_quantity_at_least_one"
            ),
        ]

    def __str__(self):
        return f"{self.quantity} × {self.variant}"
