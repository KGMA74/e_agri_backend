from urllib.parse import urlencode
from djoser.email import ActivationEmail
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class CustomActivationEmail(ActivationEmail):
    def get_context_data(self):
        context = super().get_context_data()
        self.template_name = f"accounts/emails/{'default' if context['user'].role=='admin' else context['user'].role}_activation.html"
        return context
    