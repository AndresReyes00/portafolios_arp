from django.dispatch import receiver
from .models import Notification
from django.contrib.auth.signals import user_logged_in

@receiver(user_logged_in)
def create_login_notification(sender, request, user, **kwargs):
    Notification.objects.create(
        notification_type=Notification.NotificationType.LOGIN,
        title="Nuevo inicio de sesión",
        message=f"El usuario {user.username} inició sesión.",
        user=user,
    )
