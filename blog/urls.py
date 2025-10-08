from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # CAMBIO CRUCIAL: Añadir namespace='posts'
    path('posts/', include(('posts.urls', 'posts'), namespace='posts')),
    
    path("", include(("auth_perfiles.urls", "auth_perfiles"), namespace="auth_perfiles")),
    path("", TemplateView.as_view(template_name="base.html"), name="home"),
]