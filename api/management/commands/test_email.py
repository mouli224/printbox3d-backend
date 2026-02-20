"""
Test email configuration by sending a test email.
Usage: python manage.py test_email your@email.com
"""
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings


class Command(BaseCommand):
    help = 'Send a test email to verify SMTP configuration'

    def add_arguments(self, parser):
        parser.add_argument('recipient', type=str, help='Email address to send test to')

    def handle(self, *args, **options):
        recipient = options['recipient']
        self.stdout.write(f'Sending test email to {recipient}...')
        self.stdout.write(f'  Backend : {settings.EMAIL_BACKEND}')
        self.stdout.write(f'  Host    : {settings.EMAIL_HOST}:{settings.EMAIL_PORT}')
        self.stdout.write(f'  TLS     : {settings.EMAIL_USE_TLS}')
        self.stdout.write(f'  SSL     : {getattr(settings, "EMAIL_USE_SSL", False)}')
        self.stdout.write(f'  From    : {settings.DEFAULT_FROM_EMAIL}')
        self.stdout.write(f'  User    : {settings.EMAIL_HOST_USER}')

        try:
            send_mail(
                subject='PrintBox3D — Test Email',
                message='This is a test email from PrintBox3D backend. SMTP is configured correctly!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS(f'✅ Email sent successfully to {recipient}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Failed to send email: {e}'))
