from django import forms
from my_apps.accounts.models import ContactMessage


class ContactMessageForm(forms.ModelForm):

    class Meta:
        model = ContactMessage

        fields = [
            "name",
            "email",
            "subject",
            "message",
        ]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Your name",
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Your email",
            }),

            "subject": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Subject",
            }),

            "message": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Tell me about your project...",
                "rows": 5,
            }),
        }

        labels = {
            "name": "Name",
            "email": "Email",
            "subject": "Subject",
            "message": "Message",
        }