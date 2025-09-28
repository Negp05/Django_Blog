from django.urls import path
from .views import (
    PostListView, PostDetailView,
    PostCreateView, PostUpdateView, PostDeleteView
)

app_name = "posts"

urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path("crear/", PostCreateView.as_view(), name="post_create"),
    path("<slug:slug>/", PostDetailView.as_view(), name="post_detail"),
    path("<slug:slug>/editar/", PostUpdateView.as_view(), name="post_update"),
    path("<slug:slug>/eliminar/", PostDeleteView.as_view(), name="post_delete"),
]
