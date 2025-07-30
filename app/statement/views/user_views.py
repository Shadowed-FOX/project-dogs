from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from statement.forms.user_forms import (
    PasswordChangeForm,
    UserRegistrationForm,
    UserLoginForm,
    UserUpdateForm,
)
from statement.models import Dog, User
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            # Send verification email
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            verification_link = request.build_absolute_uri(
                reverse("verify_email", kwargs={"uidb64": uid, "token": token})
            )

            send_mail(
                "Potwierdź email",
                f"Kliknij link aby zwerfyfikować konto: {verification_link}",
                "from@example.com",
                [user.email],
                fail_silently=True,
            )

            context = {"verification_link": verification_link}
            return render(request, "app/user/register_success.html", context)
        else:
            return render(request, "app/user/register.html", {"form": form})
    else:
        form = UserRegistrationForm()
    return render(request, "app/user/register.html", {"form": form})


def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("registration_verified")
    else:
        return render(request, "app/user/verification_failed.html")


def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                # Redirect to your desired page after login
                return redirect("list_notify")
            else:
                form.add_error(None, "Nie udało się zalogować")
    else:
        form = UserLoginForm()
    return render(request, "app/user/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def update_user_info(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Dane zostały zaktualizowane.")
            return redirect("account")
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, "app/user/update_info.html", {"form": form})


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            request.user.set_password(form.cleaned_data["new_password"])
            request.user.save()
            messages.success(request, "Hasło zostało zmienione. Zaloguj się ponownie.")
            return redirect("login")
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, "app/user/change_password.html", {"form": form})
