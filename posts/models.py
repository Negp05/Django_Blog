from django.db import models
from django.conf import settings
from django.urls import reverse


class Post(models.Model):
    titulo= models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contenido = models.TextField()
    publicado = models.BooleanField(default=False)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        return reverse('posts:post_detail', kwargs={'slug': self.slug})
# Create your models here.
