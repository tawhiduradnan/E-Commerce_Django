from django.db import models
from django.contrib.auth.models import User


class Address(models.Model):
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    address_line = models.CharField(max_length=255, help_text="Street / Address line")

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.address_line}, {self.city}, {self.country}"


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer_profile")
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_image = models.ImageField(upload_to="profile_images/", blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}'s Profile"
