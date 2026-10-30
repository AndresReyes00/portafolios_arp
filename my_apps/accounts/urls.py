
from django.urls import path
from my_apps.accounts import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path(
        "staff/",
        views.staff_dashboard,
        name="staff_dashboard",
    ),
    path(
        "staff/notificaciones/",
        views.staff_notifications,
        name="staff_notifications",
    ),
    path(
        "staff/notificaciones/<int:notification_id>/leida/",
        views.mark_notification_read,
        name="mark_notification_read",
    ),
    path(
        "staff/notificaciones/marcar-todas-leidas/",
        views.mark_all_notifications_read,
        name="mark_all_notifications_read",
    ),
    path(
        "staff/notificaciones/<int:pk>/eliminar/",
        views.notification_detail,
        name="notification_detail",
    )
]
