from django.conf import settings
from django.db import models


class Notification(models.Model):
    class NotificationType(models.TextChoices):
        LOGIN = "login", "Inicio de sesión"
        CONTACT = "contact", "Mensaje de contacto"

    notification_type = models.CharField(
        max_length=20,
        choices=NotificationType.choices,
    )
    title = models.CharField(max_length=150)
    message = models.TextField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="notifications",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Notificación"
        verbose_name_plural = "Notificaciones"

    def __str__(self):
        return self.title