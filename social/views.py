from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.contrib.contenttypes.models import ContentType
from .models import Reaction, Bookmark
import json
from django.db import models
from django.shortcuts import render


#Create your views here.
def _get_ct_and_id(model_label, object_id):
    # model_label como 'posts.Post' o 'comentarios.Comment'
    try:
        app_label, model_name = model_label.split('.')
        ct = ContentType.objects.get(app_label=app_label, model=model_name.lower())
        return ct, int(object_id)
    except Exception:
        return None, None

@login_required
@require_POST
def toggle_reaction(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return HttpResponseBadRequest('Invalid JSON')

    model_label = data.get('model')  # p.ej. "posts.Post"
    object_id   = data.get('id')
    kind        = data.get('kind')   # 'like', 'love', etc.

    ct, obj_id = _get_ct_and_id(model_label, object_id)
    if not ct or not kind:
        return HttpResponseBadRequest('Missing fields')

    obj, created = Reaction.objects.get_or_create(
        user=request.user, content_type=ct, object_id=obj_id, kind=kind
    )
    if not created:
        # Si ya existía, quitar reacción (toggle)
        obj.delete()
        toggled = False
    else:
        toggled = True

    # Recuento por tipo
    counts = (Reaction.objects
              .filter(content_type=ct, object_id=obj_id)
              .values('kind').order_by()
              .annotate(c=models.Count('id')))
    return JsonResponse({
        'ok': True,
        'added': toggled,
        'counts': {row['kind']: row['c'] for row in counts},
    })

@login_required
@require_POST
def toggle_bookmark(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return HttpResponseBadRequest('Invalid JSON')
    ct, obj_id = _get_ct_and_id(data.get('model'), data.get('id'))
    if not ct:
        return HttpResponseBadRequest('Missing fields')

    obj, created = Bookmark.objects.get_or_create(
        user=request.user, content_type=ct, object_id=obj_id
    )
    if not created:
        obj.delete()
        added = False
    else:
        added = True
    return JsonResponse({'ok': True, 'added': added})

@login_required
def mis_guardados(request):
    # Filtra los guardados del usuario actual
    guardados = Bookmark.objects.filter(user=request.user).select_related('content_type')
    return render(request, 'social/mis_guardados.html', {'guardados': guardados})