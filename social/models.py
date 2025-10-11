from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

#Create your models here.
User = settings.AUTH_USER_MODEL

class Reaction(models.Model):
    LIKE = 'like'
    LOVE = 'love'
    WOW  = 'wow'
    SAD  = 'sad'
    ANGRY= 'angry'
    REACTION_CHOICES = [
        (LIKE, 'Like'), (LOVE, 'Love'), (WOW, 'Wow'), (SAD, 'Sad'), (ANGRY, 'Angry'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reactions')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    kind = models.CharField(max_length=16, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 1 reacción por tipo por usuario y objeto
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'content_type', 'object_id', 'kind'],
                name='unique_reaction_per_kind'
            )
        ]

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

class Notification(models.Model):
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='actor_notifications')
    verb = models.CharField(max_length=64)  # 'reaccionó', 'comentó', etc.
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
