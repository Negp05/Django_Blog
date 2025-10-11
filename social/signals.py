from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Reaction, Notification
from django.contrib.contenttypes.models import ContentType

@receiver(post_save, sender=Reaction)
def notify_on_reaction(sender, instance, created, **kwargs):
    if not created:
        return
    target = instance.content_object
    # Si el target tiene atributo "author" o "user"
    target_author = getattr(target, 'author', None) or getattr(target, 'user', None)
    if target_author and target_author != instance.user:
        Notification.objects.create(
            to_user=target_author,
            actor=instance.user,
            verb=f'reaccionó ({instance.kind})',
            content_type=ContentType.objects.get_for_model(target.__class__),
            object_id=target.pk
        )
