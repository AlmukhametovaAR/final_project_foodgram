from .models import Subscribe


def is_subscribed(self, obj):
    """
    Function to check if a current user is subscribed to another user.
    """
    if self.context['request'].user.is_authenticated:
        user = self.context['request'].user
        is_subscribed = Subscribe.objects.filter(
            subscriber=user, subscribed_to=obj
        ).exists()
        return is_subscribed
    return False
