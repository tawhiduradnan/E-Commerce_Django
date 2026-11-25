from decimal import Decimal, InvalidOperation

from django.db.models import Count, Q
from django.shortcuts import render
from .models import Product, ProductCategory


def parse_price(value):
    if not value:
        return None
    try:
        price = Decimal(value)
    except InvalidOperation:
        return None
    return price if price.is_finite() and price >= 0 else None


def product_list(request):
    query = request.GET.get("q", "").strip()
    selected_categories = request.GET.getlist("category")
    price_min = request.GET.get("price_min", "").strip()
    price_max = request.GET.get("price_max", "").strip()
    products = (
        Product.objects.select_related("product_category")
        .prefetch_related("images", "variants")
        .annotate(
            available_variant_count=Count(
                "variants", filter=Q(variants__stock__gt=0), distinct=True
            )
        )
        .order_by("product_name")
    )
    if query:
        products = products.filter(product_name__icontains=query)

    if selected_categories:
        products = products.filter(product_category__slug__in=selected_categories)

    min_value = parse_price(price_min)
    max_value = parse_price(price_max)
    if min_value is not None:
        products = products.filter(price__gte=min_value)
    if max_value is not None:
        products = products.filter(price__lte=max_value)

    return render(
        request,
        "products/product_list.html",
        {
            "products": products,
            "query": query,
            "categories": ProductCategory.objects.order_by("category_name"),
            "selected_categories": selected_categories,
            "price_min": price_min,
            "price_max": price_max,
        },
    )
