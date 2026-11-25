from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from .models import CustomerProfile


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}! You can now log in.")
            return redirect("login")
    else:
        form = UserRegistrationForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile(request):
    # Auto-create a CustomerProfile if it doesn't exist yet
    customer_profile, created = CustomerProfile.objects.get_or_create(user=request.user)
    context = {
        "customer_profile": customer_profile,
    }
    return render(request, "accounts/profile.html", context)
