from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Visitante, Administrador
from .forms import RegistroForm, LoginForm


def get_user(user):
    if user.is_authenticated:
        try:
            if hasattr(user, "administrador"):
                return redirect("dashboard:administradores")
        except Administrador.DoesNotExist:
            pass
        try:
            if hasattr(user, "visitante"):
                return redirect("dashboard:usuarios")
        except Visitante.DoesNotExist:
            pass
    return None


def register_view(request):
    if request.user.is_authenticated:
        redirect_response = get_user(request.user)
        if redirect_response:
            return redirect_response

    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)

                return redirect("dashboard:usuarios")

            except Exception as e:
                messages.error(request, f"Erro ao criar conta: {str(e)}")
    else:
        form = RegistroForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        redirect_response = get_user(request.user)
        if redirect_response:
            return redirect_response

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                redirect_response = get_user(user)
                if redirect_response:
                    return redirect_response
            else:
                messages.error(request, "Email ou senha inválidos.")
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})


@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect("accounts:login")
