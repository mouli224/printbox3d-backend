# Email Integration Setup Guide

## Overview
PrintBox3D uses email notifications for:
- Order confirmations (sent to customer and admin)
- Custom order requests (sent to customer and admin)
- Contact form submissions (sent to customer and admin)

All notifications are sent to **info@printbox3d.com**

## Gmail Setup Instructions

### 1. Enable 2-Factor Authentication
1. Go to your Google Account: https://myaccount.google.com/
2. Navigate to Security → 2-Step Verification
3. Enable 2-Step Verification

### 2. Generate App Password
1. Go to https://myaccount.google.com/apppasswords
2. Select "Mail" and "Other (Custom name)"
3. Enter "PrintBox3D Backend"
4. Click "Generate"
5. Copy the 16-character password (format: xxxx xxxx xxxx xxxx)

### 3. Update .env File
Add these variables to your `.env` file:

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=info@printbox3d.com
EMAIL_HOST_PASSWORD=your-16-char-app-password-here
DEFAULT_FROM_EMAIL=info@printbox3d.com
```

**Important:** Use the App Password, NOT your regular Gmail password!

## Email Notifications

### Order Confirmation
**Triggered:** After successful payment verification
**Recipients:**
- Customer: Order details, tracking info, next steps
- Admin (info@printbox3d.com): New order alert with full details

**Content:**
- Order ID
- Items ordered (name, quantity, price)
- Total amount
- Shipping address
- Contact information
- Next steps

### Custom Order Request
**Triggered:** When customer submits custom order form
**Recipients:**
- Customer: Acknowledgment of request
- Admin (info@printbox3d.com): New custom order details

**Content:**
- Request ID
- Customer details
- Material, color, quantity requirements
- Description
- Design file status
- Budget information

### Contact Form
**Triggered:** When customer submits contact form
**Recipients:**
- Customer: Acknowledgment of message
- Admin (info@printbox3d.com): New contact message

**Content:**
- Customer name and email
- Subject
- Message content

## Testing Email Configuration

### Test in Django Shell
```python
python manage.py shell

from django.core.mail import send_mail
from django.conf import settings

send_mail(
    'Test Email',
    'This is a test email from PrintBox3D',
    settings.DEFAULT_FROM_EMAIL,
    ['info@printbox3d.com'],
    fail_silently=False,
)
```

### Test with Real Order
1. Place a test order through the frontend
2. Complete payment (use Razorpay test mode)
3. Check both customer and info@printbox3d.com inboxes

## Troubleshooting

### Emails Not Sending
1. **Check .env variables:** Ensure all EMAIL_* variables are set correctly
2. **Verify App Password:** Make sure you're using the App Password, not regular password
3. **Check Gmail settings:** Ensure 2FA is enabled and App Password is active
4. **Check Django logs:** Look for email-related errors in console output
5. **Test SMTP connection:**
   ```python
   python manage.py shell
   from django.core.mail import get_connection
   connection = get_connection()
   connection.open()  # Should return True if successful
   ```

### Emails Going to Spam
1. Configure SPF record for your domain
2. Set up DKIM authentication
3. Use consistent FROM email address
4. Avoid spam trigger words

### Common Errors

**`SMTPAuthenticationError: Username and Password not accepted`**
- Solution: Generate a new App Password and update .env

**`SMTPException: STARTTLS extension not supported`**
- Solution: Verify EMAIL_USE_TLS=True and EMAIL_PORT=587

**`Connection refused`**
- Solution: Check if firewall is blocking port 587

## Production Deployment

### Railway/Supabase
1. Add email environment variables in Railway dashboard
2. Test email sending after deployment
3. Monitor email delivery logs

### Custom Domain Email
If using custom domain (e.g., info@printbox3d.com with custom hosting):
1. Update EMAIL_HOST to your mail server
2. Update EMAIL_PORT (usually 465 for SSL, 587 for TLS)
3. Update EMAIL_USE_TLS or EMAIL_USE_SSL accordingly
4. Add credentials to .env

## Email Templates
Email content is generated in `api/email_utils.py`. To customize:
1. Edit message templates in `email_utils.py`
2. Maintain customer and admin versions
3. Test changes thoroughly

## Support
For email configuration issues:
- Check Django documentation: https://docs.djangoproject.com/en/4.2/topics/email/
- Gmail SMTP guide: https://support.google.com/mail/answer/7126229
- Contact: support@printbox3d.com
