from django.contrib import admin
from .models import Post, Comentario, Like

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'publicado', 'creado', 'contador_likes', 'contador_comentarios']
    list_filter = ['publicado', 'creado', 'autor']
    search_fields = ['titulo', 'contenido']
    
    def contador_likes(self, obj):
        return obj.likes.count()
    contador_likes.short_description = 'Likes'
    
    def contador_comentarios(self, obj):
        return obj.comentarios.count()
    contador_comentarios.short_description = 'Comentarios'

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['autor', 'post', 'creado', 'activo']
    list_filter = ['activo', 'creado']

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'post', 'creado']