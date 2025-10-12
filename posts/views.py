from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .forms import PostForm
from .models import Post  # tu modelo de post
from social.models import Reaction  # importar el modelo de reacciones
from django.db.models import Count, Q, Exists, OuterRef, Value, BooleanField
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, get_object_or_404
from social.models import Bookmark


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    is_bookmarked = False
    if request.user.is_authenticated:
        ct = ContentType.objects.get_for_model(Post)
        is_bookmarked = Bookmark.objects.filter(
            user=request.user, content_type=ct, object_id=post.id
        ).exists()

    return render(request, 'post_detail.html', {
        'post': post,
        'is_bookmarked': is_bookmarked,
    })

#reacciones
def post_list(request):
    qs = Post.objects.filter(publicado=True).order_by('-creado')

    if not request.user.is_authenticated:
        qs = qs.annotate(is_bookmarked=Value(False, output_field=BooleanField()))
    else:
        ct = ContentType.objects.get_for_model(Post)
        bookmarks = Bookmark.objects.filter(
            user=request.user,
            content_type=ct,
            object_id=OuterRef('pk'),
        )
        qs = qs.annotate(is_bookmarked=Exists(bookmarks))

    return render(request, 'posts/post_list.html', {'posts': qs})

# Lista general (pública)
class PostListView(ListView):
    model = Post
    template_name = "posts/post_list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        qs = Post.objects.filter(publicado=True).order_by("-creado")

        if not self.request.user.is_authenticated:
            return qs.annotate(is_bookmarked=Value(False, output_field=BooleanField()))

        ct = ContentType.objects.get_for_model(Post)
        bookmarks = Bookmark.objects.filter(
            user=self.request.user,
            content_type=ct,
            object_id=OuterRef('pk'),
        )
        return qs.annotate(is_bookmarked=Exists(bookmarks))



class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        post = self.object

        # ¿ya está guardado por el usuario actual?
        is_bookmarked = False
        if self.request.user.is_authenticated:
            ct = ContentType.objects.get_for_model(Post)
            is_bookmarked = Bookmark.objects.filter(
                user=self.request.user,
                content_type=ct,
                object_id=post.id
            ).exists()
        ctx["is_bookmarked"] = is_bookmarked

        # (Opcional) Conteos de reacciones para render inicial
        ct_post = ContentType.objects.get_for_model(Post)
        rows = (Reaction.objects
                .filter(content_type=ct_post, object_id=post.id)
                .values('kind').annotate(c=Count('id')))
        ctx["reaction_counts"] = {r["kind"]: r["c"] for r in rows}

        return ctx



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