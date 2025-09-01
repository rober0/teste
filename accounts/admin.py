from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Visitante, Administrador, Usuarios


class CustomUserAdmin(UserAdmin):
    ordering = ("email",)
    list_display = ("email", "username", "is_staff", "is_active")
    search_fields = ("email", "username")

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        (
            "Permissões",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Datas", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password", "password_confirm"),
            },
        ),
    )


class VisitanteAdmin(CustomUserAdmin):
    list_display = (
        "username",
        "email",
        "avatar",
        "data_nascimento",
        "genero",
    )

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Informações Pessoais",
            {"fields": ("username", "avatar", "data_nascimento", "genero")},
        ),
        ("Permissões", {"fields": ("is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "avatar",
                    "data_nascimento",
                    "genero",
                    "password",
                    "password_confirm",
                ),
            },
        ),
    )


class AdministradorAdmin(CustomUserAdmin):
    list_display = ("username", "email", "avatar", "is_staff", "is_superuser")

    fieldsets = (
        (None, {"fields": ("username", "email", "avatar", "password")}),
        (
            "Permissões",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "avatar",
                    "password",
                    "password_confirm",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


admin.site.register(Visitante, VisitanteAdmin)
admin.site.register(Administrador, AdministradorAdmin)
admin.site.register(Usuarios, CustomUserAdmin)
