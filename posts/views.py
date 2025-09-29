from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .forms import PostForm



# Lista general (pública)
class PostListView(ListView):
    model = Post
    template_name = "posts/post_list.html"
    context_object_name = "posts"             # <- antes 'post', ahora 'posts'
    paginate_by = 10
    queryset = Post.objects.filter(publicado=True).order_by("-creado")


class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    context_object_name = "post"


# Mis posts (del usuario autenticado)
class MyPostsListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "posts/post_list.html"    # reutilizamos el mismo listado
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(autor=self.request.user).order_by("-creado")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["mine"] = True                    # para que la plantilla cambie el título si quieres
        return ctx


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["titulo", "slug", "contenido", "publicado"]
    template_name = "posts/post_form.html"
    context_object_name = "post"

    def form_valid(self, form):
        form.instance.autor = self.request.user
        messages.success(self.request, "Post creado correctamente.")
        resp = super().form_valid(form)
        return resp

    def get_success_url(self):
        # Redirige al detalle del post recién creado
        return reverse("posts:post_detail", kwargs={"slug": self.object.slug})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["titulo", "slug", "contenido", "publicado"] 
    template_name = "posts/post_form.html"
    context_object_name = "post"

    def test_func(self):
        post = self.get_object()
        return post.autor == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Post actualizado correctamente.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("posts:post_detail", kwargs={"slug": self.object.slug})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "posts/post_confirm_delete.html"
    success_url = reverse_lazy("posts:post_list")
    context_object_name = "post"

    def test_func(self):
        post = self.get_object()
        return post.autor == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Post eliminado correctamente.")
        return super().delete(request, *args, **kwargs)
