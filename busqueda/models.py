from django.db import models
from django.contrib.auth.models import User
from posts.models import Post  # Importa el modelo de Post

class EmojiReaction(models.Model):
    EMOJI_CHOICES = [
        ("👍", "Like"),
        ("❤️", "Love"),
        ("😂", "Laugh"),
        ("😮", "Wow"),
        ("😢", "Sad"),
        ("😡", "Angry"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="emoji_reactions")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="emoji_reactions")
    emoji = models.CharField(max_length=5, choices=EMOJI_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post", "emoji")  # evita reacciones duplicadas del mismo emoji

    def __str__(self):
        return f"{self.user.username} reaccionó con {self.emoji} en {self.post}"
