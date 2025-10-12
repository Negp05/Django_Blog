from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('mis/', views.MyPostsListView.as_view(), name='mis_posts'),
    path('crear/', views.PostCreateView.as_view(), name='post_create'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('<slug:slug>/editar/', views.PostUpdateView.as_view(), name='post_update'),
    path('<slug:slug>/eliminar/', views.PostDeleteView.as_view(), name='post_delete'),
    path('', views.post_list, name='post_list'),

]