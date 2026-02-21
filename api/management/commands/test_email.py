"""
Test email configuration by sending a test email.
Usage: python manage.py test_email your@email.com
"""
import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from api.email_utils import _send_email


class Command(BaseCommand):
    help = 'Send a test email and show detailed diagnostics (Resend API or SMTP)'

    def add_arguments(self, parser):
        parser.add_argument('recipient', type=str, help='Email address to send test to')

    def handle(self, *args, **options):
        recipient = options['recipient']
        resend_key = getattr(settings, 'RESEND_API_KEY', '')
        from_email = settings.DEFAULT_FROM_EMAIL

        self.stdout.write('=' * 60)
        self.stdout.write('PrintBox3D Email Diagnostics')
        self.stdout.write('=' * 60)

        if resend_key:
            self.stdout.write(f'  Mode       : Resend API')
            self.stdout.write(f'  Key prefix : {resend_key[:10]}...')
            self.stdout.write(f'  From       : {from_email}')
            self.stdout.write(f'  To         : {recipient}')
            self.stdout.write('')
            self.stdout.write('Calling Resend API directly...')
            try:
                resp = requests.post(
                    'https://api.resend.com/emails',
                    headers={
                        'Authorization': f'Bearer {resend_key}',
                        'Content-Type': 'application/json',
                    },
                    json={
                        'from': from_email,
                        'to': [recipient],
                        'subject': 'PrintBox3D — Test Email',
                        'text': 'Test email from PrintBox3D. If you receive this, email is working!',
                    },
                    timeout=30,
                )
                self.stdout.write(f'  HTTP Status : {resp.status_code}')
                self.stdout.write(f'  Response    : {resp.text}')
                if resp.ok:
                    self.stdout.write(self.style.SUCCESS('✅ Resend API: email sent successfully!'))
                else:
                    self.stdout.write(self.style.ERROR('❌ Resend API returned an error (see response above)'))
                    self.stdout.write('')
                    self.stdout.write('Common fixes:')
                    self.stdout.write('  422 validation_error  → domain not verified in Resend dashboard')
                    self.stdout.write('  401 missing_api_key   → RESEND_API_KEY env var not set correctly')
                    self.stdout.write('  403 not_allowed       → sending domain not added/verified in Resend')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Network error calling Resend: {e}'))
        else:
            self.stdout.write(f'  Mode    : SMTP (no RESEND_API_KEY set)')
            self.stdout.write(f'  Host    : {settings.EMAIL_HOST}:{settings.EMAIL_PORT}')
            self.stdout.write(f'  TLS     : {settings.EMAIL_USE_TLS}')
            self.stdout.write(f'  SSL     : {getattr(settings, "EMAIL_USE_SSL", False)}')
            self.stdout.write(f'  From    : {from_email}')
            self.stdout.write(f'  To      : {recipient}')
            self.stdout.write('')
            self.stdout.write('WARNING: SMTP ports 465/587 are often blocked on cloud platforms.')
            self.stdout.write('         Set RESEND_API_KEY in Railway env vars to fix this.')
            self.stdout.write('')
            try:
                _send_email(
                    to=recipient,
                    subject='PrintBox3D — Test Email',
                    text='Test email from PrintBox3D. If you receive this, SMTP is working!',
                )
                self.stdout.write(self.style.SUCCESS(f'✅ SMTP: email sent successfully to {recipient}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ SMTP failed: {e}'))
