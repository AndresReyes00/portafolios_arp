from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Notification
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.utils import timezone


class UserLoginView(LoginView):
    template_name = "accounts/login.html"


class UserRegisterView(CreateView):
    template_name = "accounts/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("accounts:login")


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("home")



@staff_member_required
def staff_dashboard(request):
    today = timezone.localdate()

    notifications = Notification.objects.select_related(
        "user"
    )

    login_notifications = notifications.filter(
        notification_type=Notification.NotificationType.LOGIN
    )

    contact_notifications = notifications.filter(
        notification_type=Notification.NotificationType.CONTACT
    )

    context = {
        "total_logins_today": login_notifications.filter(
            created_at__date=today
        ).count(),

        "total_messages": contact_notifications.count(),

        "unread_count": notifications.filter(
            is_read=False
        ).count(),

        "total_notifications": notifications.count(),

        "recent_activity": notifications[:8],

        "recent_messages": contact_notifications[:5],

        "today": today,
    }

    return render(
        request,
        "accounts/dashboard.html",
        context,
    )

@staff_member_required
def staff_notifications(request):
    notifications = Notification.objects.select_related(
        "user"
    )

    filter_type = request.GET.get("type", "all")

    if filter_type == "unread":
        notifications = notifications.filter(is_read=False)

    elif filter_type == "login":
        notifications = notifications.filter(
            notification_type=Notification.NotificationType.LOGIN
        )

    elif filter_type == "contact":
        notifications = notifications.filter(
            notification_type=Notification.NotificationType.CONTACT
        )

    context = {
        "notifications": notifications,

        "total_count": Notification.objects.count(),

        "unread_count": Notification.objects.filter(
            is_read=False
        ).count(),

        "read_count": Notification.objects.filter(
            is_read=True
        ).count(),

        "filter_type": filter_type,
    }

    return render(
        request,
        "accounts/notifications.html",
        context,
    )



@staff_member_required
@require_POST
def mark_all_notifications_read(request):
    Notification.objects.filter(
        is_read=False
    ).update(is_read=True)

    return redirect("accounts:staff_notifications")

@staff_member_required
@require_POST
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(
        Notification,
        pk=notification_id,
    )
    notification.is_read = True
    notification.save(update_fields=["is_read"])

    return redirect("accounts:staff_notifications")


@staff_member_required
def notification_detail(request, pk):

    notification = get_object_or_404(
        Notification.objects.select_related(
            "user",
            "contact_message"
        ),
        pk=pk
    )

    # Mark notification as read
    if not notification.is_read:
        notification.is_read = True
        notification.save(update_fields=["is_read"])

    context = {
        "notification": notification,
        "contact_message": notification.contact_message,
    }

    return render(
        request,
        "accounts/notification_detail.html",
        context
    )


