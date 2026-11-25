from django.contrib import admin
from .models import Address, CustomerProfile


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("address_line", "city", "postal_code", "country")
    search_fields = ("address_line", "city", "country", "postal_code")


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "address")
    search_fields = ("user__username", "user__email", "phone")
    raw_id_fields = ("user",)
