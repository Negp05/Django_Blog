from django.urls import path
from . import views

app_name = 'social'
urlpatterns = [
    path('reaction/toggle/', views.toggle_reaction, name='toggle_reaction'),
    path('bookmark/toggle/', views.toggle_bookmark, name='toggle_bookmark'),
    path('mis-guardados/', views.mis_guardados, name='mis_guardados'),
]
