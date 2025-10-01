from django.contrib import admin
from .models import Post # Asegúrate de que solo importas 'Post'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Ya no listamos 'contador_likes' ni 'contador_comentarios'
    list_display = ['titulo', 'autor', 'publicado', 'creado']
    list_filter = ['publicado', 'creado', 'autor']
    search_fields = ['titulo', 'contenido']
    
    # Eliminamos las funciones contador_likes y contador_comentarios
    # y ya no registramos los otros modelos.