from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post

class PostListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'
    queryset = Post.objects.filter(publicado=True).order_by('-creado')
    paginate_by = 10
    context_object_name = 'post'

class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['titulo', 'slug', 'contenido', 'publicado']
    template_name = 'posts/post_form.html'
    context_object_name = 'post'

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['titulo', 'slug', 'contenido', 'publicado']
    template_name = 'posts/post_form.html'
    context_object_name = 'post'

    def test_func(self):
        post = self.get_object()
        return post.autor == self.request.user

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('posts:post_list')
    context_object_name = 'post'

    def test_func(self):
        post = self.get_object()
        return post.autor == self.request.user



