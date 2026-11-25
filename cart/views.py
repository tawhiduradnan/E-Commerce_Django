from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from products.models import Product, ProductVariant

from .models import Cart, CartItem


@login_required
def add_to_cart(request, product_id):
    if request.method != "POST":
        return redirect("home")

    product = get_object_or_404(Product, pk=product_id)
    variant_id = request.POST.get("variant")
    try:
        quantity = int(request.POST.get("quantity", "1"))
    except (TypeError, ValueError):
        quantity = 0

    if quantity < 1:
        messages.error(request, "Choose a quantity of at least 1.")
        return redirect("home")

    with transaction.atomic():
        variant = get_object_or_404(
            ProductVariant.objects.select_for_update(),
            pk=variant_id,
            product=product,
        )
        cart, _ = Cart.objects.get_or_create(customer=request.user)
        item, created = CartItem.objects.get_or_create(
            cart=cart, variant=variant, defaults={"quantity": quantity}
        )
        requested_total = quantity if created else item.quantity + quantity

        if variant.stock < requested_total:
            available_to_add = max(variant.stock - (0 if created else item.quantity), 0)
            if created:
                item.delete()
            messages.error(
                request,
                f"Only {available_to_add} more of {variant} available. "
                "Your cart was not changed.",
            )
        else:
            if not created:
                item.quantity = requested_total
                item.save(update_fields=["quantity"])
            messages.success(request, f"Added {quantity} × {variant} to your cart.")

    return redirect("cart:view")


@login_required
def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(customer=request.user)
    items = list(
        cart.items.select_related("variant__product").order_by("variant__product__product_name")
    )
    total = 0
    for item in items:
        item.line_total = item.variant.product.price * item.quantity
        total += item.line_total

    return render(request, "cart/cart_detail.html", {"cart": cart, "items": items, "total": total})


@login_required
def update_cart_item(request, item_id):
    if request.method != "POST":
        return redirect("cart:view")

    with transaction.atomic():
        item_variant = get_object_or_404(
            CartItem.objects.only("variant_id"),
            pk=item_id,
            cart__customer=request.user,
        )
        variant = ProductVariant.objects.select_for_update().get(
            pk=item_variant.variant_id
        )
        item = get_object_or_404(
            CartItem.objects.select_for_update(),
            pk=item_id,
            cart__customer=request.user,
        )
        try:
            quantity = int(request.POST.get("quantity", "0"))
        except (TypeError, ValueError):
            quantity = 0

        if quantity <= 0:
            item.delete()
            messages.success(request, "Item removed from your cart.")
        else:
            if quantity > variant.stock:
                messages.error(request, f"Only {variant.stock} of {variant} are currently in stock.")
            else:
                item.quantity = quantity
                item.save(update_fields=["quantity"])

    return redirect("cart:view")


@login_required
def remove_cart_item(request, item_id):
    if request.method == "POST":
        CartItem.objects.filter(pk=item_id, cart__customer=request.user).delete()
        messages.success(request, "Item removed from your cart.")
    return redirect("cart:view")
