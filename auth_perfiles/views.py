from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.http import url_has_allowed_host_and_scheme


# --- Registro ---
class RegisterForm(forms.ModelForm):
    # Usar los nombres de campo que definiste
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repite la contraseña", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email"]

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Las contraseñas no coinciden")
        return cleaned

    def save(self, commit=True):
        # Crear la instancia del usuario, solo con username y email
        user = User(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
        )
        # Establecer la contraseña de forma segura
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cuenta creada. Ahora inicia sesión.")
            return redirect("auth_perfiles:login")
        else:
            messages.error(request, "Revisa los errores del formulario.")
    else:
        form = RegisterForm()
    return render(request, "auth_perfiles/register.html", {"form": form})


# --- Login ---
def login_view(request):
    next_url = request.GET.get("next") or request.POST.get("next")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)

            # "Recuérdame": si NO está marcado, expira al cerrar el navegador
            if not request.POST.get("remember_me"):
                request.session.set_expiry(0)

            messages.success(request, "Sesión iniciada.")

            # Respeta ?next= si es una URL segura del mismo host
            if next_url and url_has_allowed_host_and_scheme(
                next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()
            ):
                return redirect(next_url)

            # FALLBACK CORREGIDO: Redirige a 'posts:post_list' (el nombre correcto)
            return redirect("posts:post_list")

        messages.error(request, "Usuario o contraseña incorrectos.")

    return render(request, "auth_perfiles/login.html", {"next": next_url})


# --- Logout ---
def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "Has cerrado sesión.")
    return redirect("home")
