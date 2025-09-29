from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["titulo", "slug", "contenido", "publicado"]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control", "placeholder": "Título"}),
            "slug": forms.TextInput(attrs={"class": "form-control", "placeholder": "mi-post"}),
            "contenido": forms.Textarea(attrs={"class": "form-control", "rows": 6}),
            "publicado": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.is_bound:
            for name, field in self.fields.items():
                if self[name].errors:
                    field.widget.attrs["class"] = (
                        field.widget.attrs.get("class", "") + " is-invalid"
                    ).strip()
