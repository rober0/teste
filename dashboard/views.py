from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.decorators import admin_required, visitante_required


@login_required
@visitante_required
def visitante(request):
    return render(request, "dashboard/usuario.html")


@login_required
@admin_required
def administrador(request):
    return render(request, "dashboard/administrador.html")
