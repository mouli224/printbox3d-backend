"""
Razorpay Service — PrintBox3D
Centralises all Razorpay interactions so views stay thin.

Usage:
    from api.services.razorpay_service import RazorpayService
    order  = RazorpayService.create_order(amount_inr=299, receipt='ORD123')
    valid  = RazorpayService.verify_signature(order_id, payment_id, signature)
"""

import hmac
import hashlib
import logging

import razorpay
from django.conf import settings

logger = logging.getLogger(__name__)


def _get_client() -> razorpay.Client:
    """
    Initialise and return an authenticated Razorpay client.

    Raises:
        ValueError: if credentials are missing from settings.
    """
    key_id = getattr(settings, 'RAZORPAY_KEY_ID', '')
    key_secret = getattr(settings, 'RAZORPAY_KEY_SECRET', '')

    if not key_id or not key_secret:
        raise ValueError(
            "Razorpay credentials (RAZORPAY_KEY_ID / RAZORPAY_KEY_SECRET) "
            "are not configured in settings."
        )

    return razorpay.Client(auth=(key_id, key_secret))


class RazorpayService:
    """Encapsulates all Razorpay API calls and signature verification."""

    @staticmethod
    def create_order(amount_inr: float, receipt: str, notes: dict | None = None) -> dict:
        """
        Create a Razorpay order.

        Args:
            amount_inr: Total amount in Indian Rupees (will be converted to paise).
            receipt:    Unique receipt identifier (e.g. internal order_id).
            notes:      Optional key-value metadata dict.

        Returns:
            Razorpay order dict, e.g.:
            {
                'id':       'order_XXXXXX',
                'amount':   29900,        # paise
                'currency': 'INR',
                ...
            }

        Raises:
            ValueError:   If credentials are missing.
            RuntimeError: If Razorpay API call fails.
        """
        amount_paise = int(amount_inr * 100)

        payload = {
            'amount': amount_paise,
            'currency': 'INR',
            'receipt': receipt,
            'payment_capture': 1,  # Auto-capture on payment success
        }
        if notes:
            payload['notes'] = notes

        try:
            client = _get_client()
            rz_order = client.order.create(payload)
            logger.info(
                f"[Razorpay] Order created → id={rz_order['id']}, "
                f"amount={amount_paise} paise, receipt={receipt}"
            )
            return rz_order
        except ValueError:
            raise
        except Exception as exc:
            logger.error(f"[Razorpay] create_order failed: {exc}", exc_info=True)
            raise RuntimeError(f"Razorpay order creation failed: {exc}") from exc

    @staticmethod
    def verify_signature(
        razorpay_order_id: str,
        razorpay_payment_id: str,
        razorpay_signature: str,
    ) -> bool:
        """
        Verify a Razorpay payment signature (HMAC-SHA256).

        This MUST be called server-side only.  Never trust a frontend
        success callback without running this check.

        Args:
            razorpay_order_id:  The order_id returned by Razorpay.
            razorpay_payment_id: The payment_id returned after payment.
            razorpay_signature:  The signature returned by Razorpay.

        Returns:
            True if the signature is valid, False otherwise.

        Raises:
            ValueError: If RAZORPAY_KEY_SECRET is not configured.
        """
        key_secret = getattr(settings, 'RAZORPAY_KEY_SECRET', '')
        if not key_secret:
            raise ValueError("RAZORPAY_KEY_SECRET is not configured.")

        message = f"{razorpay_order_id}|{razorpay_payment_id}"
        generated = hmac.new(
            key_secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256,
        ).hexdigest()

        valid = hmac.compare_digest(generated, razorpay_signature)

        if valid:
            logger.info(
                f"[Razorpay] Signature verified ✓ payment={razorpay_payment_id}"
            )
        else:
            logger.warning(
                f"[Razorpay] Signature MISMATCH ✗ payment={razorpay_payment_id}"
            )

        return valid

    @staticmethod
    def verify_webhook_signature(webhook_body: bytes, webhook_signature: str) -> bool:
        """
        Verify a Razorpay webhook payload signature.

        Use this on the /api/payments/webhook/ endpoint.

        Args:
            webhook_body:      Raw request body bytes.
            webhook_signature: Value of the 'X-Razorpay-Signature' header.

        Returns:
            True if valid, False otherwise.
        """
        webhook_secret = getattr(settings, 'RAZORPAY_WEBHOOK_SECRET', '')
        if not webhook_secret:
            logger.warning("[Razorpay] RAZORPAY_WEBHOOK_SECRET not set — skipping webhook verification")
            return False

        generated = hmac.new(
            webhook_secret.encode('utf-8'),
            webhook_body,
            hashlib.sha256,
        ).hexdigest()

        return hmac.compare_digest(generated, webhook_signature)

    @staticmethod
    def is_configured() -> bool:
        """Return True if Razorpay credentials are present in settings."""
        return bool(
            getattr(settings, 'RAZORPAY_KEY_ID', '') and
            getattr(settings, 'RAZORPAY_KEY_SECRET', '')
        )
