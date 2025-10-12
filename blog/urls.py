from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views  # ← IMPORTANTE: Agrega esto

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # CAMBIO CRUCIAL: Añadir namespace='posts'
    path('posts/', include(('posts.urls', 'posts'), namespace='posts')),
    
    path("", include(("auth_perfiles.urls", "auth_perfiles"), namespace="auth_perfiles")),
    path("", TemplateView.as_view(template_name="base.html"), name="home"),
    
    # === AGREGA ESTAS RUTAS DE AUTENTICACIÓN ===
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]