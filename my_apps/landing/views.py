from django.views import View
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db import transaction

from django.utils.decorators import method_decorator

from .forms import ContactMessageForm
from my_apps.accounts.models import Notification


class HomeView(View):

    def get(self, request):
        return render(request, "landing/index.html")


@require_POST
def contact_view(request):

    form = ContactMessageForm(request.POST)

    if form.is_valid():

        with transaction.atomic():

            contact_message = form.save()

            Notification.objects.create(
                notification_type=Notification.NotificationType.CONTACT,
                title="Nuevo mensaje de contacto",
                message=f"{contact_message.name}: {contact_message.subject}",
                contact_message=contact_message,
            )

        messages.success(
            request,
            "Message sent successfully!"
        )

    else:
        print("FORM ERRORS:", form.errors)

        messages.error(
            request,
            "Please check the submitted information."
        )

    return redirect("landing:home")