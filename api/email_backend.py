"""
Custom SMTP email backend that skips SSL certificate verification.
Needed for Hostinger SMTP on some environments where their cert chain
fails Python's strict verification.
"""
import ssl
from django.core.mail.backends.smtp import EmailBackend as DjangoSMTPBackend


class HostingerEmailBackend(DjangoSMTPBackend):
    def open(self):
        if self.connection:
            return False
        try:
            # Create a permissive SSL context that skips cert verification
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

            import smtplib
            if self.use_ssl:
                self.connection = smtplib.SMTP_SSL(
                    self.host, self.port,
                    timeout=self.timeout,
                    context=ssl_context,
                )
            else:
                self.connection = smtplib.SMTP(
                    self.host, self.port,
                    timeout=self.timeout,
                )
                self.connection.ehlo()
                if self.use_tls:
                    self.connection.starttls(context=ssl_context)
                    self.connection.ehlo()

            if self.username and self.password:
                self.connection.login(self.username, self.password)

            return True
        except Exception:
            if not self.fail_silently:
                raise
