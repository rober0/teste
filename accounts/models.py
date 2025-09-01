from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import validate_email, RegexValidator
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email é obrigatório")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        if not password:
            raise ValueError("A senha é obrigatório para superusuário")

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("username")

        user = self.create_user(email=email, password=password, **extra_fields)

        try:
            admin = Administrador.objects.create(
                usuarios_ptr=user, email=user.email, username=user.username
            )
            admin.is_staff = True
            admin.is_superuser = True
            admin.set_password(password)
            admin.save()

            return admin
        except Exception as e:
            user.delete()
            raise e


class Usuarios(AbstractUser):
    email = models.EmailField(_("Email"), unique=True, validators=[validate_email])
    username = models.CharField(
        _("username"),
        max_length=255,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$",
            )
        ],
    )
    avatar = models.ImageField(
        upload_to="avatars", default="/avatars/default.png", blank=True
    )

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def save(self, *args, **kwargs):
        if self.username:
            self.username = self.username.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username}"


class Administrador(Usuarios):
    class Meta:
        verbose_name = "Administrador"
        verbose_name_plural = "Administradores"

    def __str__(self):
        return f"{self.username}"


class Visitante(Usuarios):
    data_nascimento = models.DateField(null=False, blank=False)
    genero = models.CharField(max_length=20, null=False, blank=False)

    class Meta:
        verbose_name = "Visitante"
        verbose_name_plural = "Visitantes"

    def __str__(self):
        return f"{self.username}"
