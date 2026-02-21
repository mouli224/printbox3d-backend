"""
Test email configuration by sending a test email.
Usage: python manage.py test_email your@email.com
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from api.email_utils import _send_email


class Command(BaseCommand):
    help = 'Send a test email to verify email configuration (Resend API or SMTP)'

    def add_arguments(self, parser):
        parser.add_argument('recipient', type=str, help='Email address to send test to')

    def handle(self, *args, **options):
        recipient = options['recipient']
        resend_key = getattr(settings, 'RESEND_API_KEY', '')
        self.stdout.write(f'Sending test email to {recipient}...')
        if resend_key:
            self.stdout.write(f'  Mode    : Resend API (key set)')
        else:
            self.stdout.write(f'  Mode    : SMTP')
            self.stdout.write(f'  Host    : {settings.EMAIL_HOST}:{settings.EMAIL_PORT}')
            self.stdout.write(f'  TLS     : {settings.EMAIL_USE_TLS}')
            self.stdout.write(f'  SSL     : {getattr(settings, "EMAIL_USE_SSL", False)}')
        self.stdout.write(f'  From    : {settings.DEFAULT_FROM_EMAIL}')

        try:
            _send_email(
                to=recipient,
                subject='PrintBox3D — Test Email',
                text='This is a test email from PrintBox3D backend. Email is configured correctly!',
            )
            self.stdout.write(self.style.SUCCESS(f'✅ Email sent successfully to {recipient}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Failed to send email: {e}'))
