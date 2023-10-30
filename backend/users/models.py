from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Subscribe(models.Model):
    subscriber = models.ForeignKey(
        User,
        verbose_name='subscriber',
        help_text='User who subscribes',
        on_delete=models.CASCADE,
        related_name='subscriber'
    )
    subscribed_to = models.ForeignKey(
        User,
        verbose_name='subscribed_to',
        help_text='User being subscribed to',
        on_delete=models.CASCADE,
        related_name='subscribed_to'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='subscribe_unique_relationships',
                fields=['subscriber', 'subscribed_to'],
            )
        ]

    def __str__(self) -> str:
        return self.subscriber
