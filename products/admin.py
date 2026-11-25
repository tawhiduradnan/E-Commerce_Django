from django.contrib import admin
from .models import ProductCategory, Product, ProductImage, ProductVariant


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("category_name", "slug")
    prepopulated_fields = {"slug": ("category_name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("product_name", "product_category", "price")
    list_filter = ("product_category",)
    search_fields = ("product_name", "description")
    prepopulated_fields = {"slug": ("product_name",)}
    inlines = [ProductImageInline, ProductVariantInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "image")


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ("product", "name", "color", "storage_size", "stock")
    list_filter = ("product", "color")
    search_fields = ("name",)
