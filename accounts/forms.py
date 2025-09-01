from django import forms
from .models import Visitante, Usuarios
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate


class RegistroForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "type": "password",
                "required placeholder": "Senha",
                "class": "input validator",
                "minlength": "8",
                "title": "Must be more than 8 characters, including number, lowercase letter, uppercase letter",
            }
        ),
        validators=[validate_password],
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "type": "password",
                "required placeholder": "Confirme a Senha",
                "class": "input validator",
                "minlength": "8",
                "title": "Must be more than 8 characters, including number, lowercase letter, uppercase letter",
            }
        ),
        validators=[validate_password],
    )

    class Meta:
        model = Visitante
        fields = ["username", "email", "data_nascimento", "genero"]
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "type": "text",
                    "class": "input validator",
                    "name": "username",
                    "required placeholder": "Nome",
                    "minlength": "3",
                    "title": "Must be more than 3 characters, only letters and spaces",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "type": "email",
                    "class": "input validator",
                    "placeholder": "abc@gmail.com",
                    "required": "required",
                }
            ),
            "data_nascimento": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "input validator",
                    "min": "1935-01-01",
                    "max": "2025-12-31",
                    "title": "Must be valid",
                }
            ),
            "genero": forms.Select(
                attrs={"class": "select validator", "required": "required"},
                choices=[
                    ("", ""),
                    ("Masculino", "Masculino"),
                    ("Feminino", "Feminino"),
                    ("Outro", "Outro"),
                ],
            ),
        }

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if Usuarios.objects.filter(username=username).exists():
            raise ValidationError("Este nome já está em uso.")

        return username

    def clean_password(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")

        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError("As senhas não coincidem")
        return password

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if Usuarios.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email já está em uso.")

        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "type": "email",
                "class": "input validator",
                "placeholder": "abc@gmail.com",
                "required": "required",
            }
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "type": "password",
                "required placeholder": "Senha",
                "class": "input validator",
                "minlength": "8",
                "title": "Must be more than 8 characters, including number, lowercase letter, uppercase letter",
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                self.add_error(None, "Email ou senha inválidos.")
            else:
                self.user = user
        return cleaned_data
