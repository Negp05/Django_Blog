from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
import uuid

class Post(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contenido = models.TextField()
    publicado = models.BooleanField(default=False)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo
    
    def save(self, *args, **kwargs):
        # Generar slug automáticamente del título
        if not self.slug:
            self.slug = slugify(self.titulo)
            
            # Si el slug ya existe, agregar un identificador único
            if Post.objects.filter(slug=self.slug).exists():
                self.slug = f"{self.slug}-{uuid.uuid4().hex[:8]}"
                
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('posts:post_detail', kwargs={'slug': self.slug})

class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contenido = models.TextField(max_length=1000)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['creado']

    def __str__(self):
        return f'Comentario de {self.autor} en {self.post.titulo}'

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['post', 'usuario']

    def __str__(self):
        return f'{self.usuario.username} likes {self.post.titulo}'