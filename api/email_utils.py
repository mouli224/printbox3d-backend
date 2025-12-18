from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags


def send_order_confirmation_email(order):
    """
    Send order confirmation email to customer
    """
    subject = f'Order Confirmation - PrintBox3D #{order.order_id}'
    
    # Prepare order items details
    items_details = []
    for item in order.items.all():
        items_details.append({
            'name': item.product_name,
            'quantity': item.quantity,
            'price': item.product_price,
            'subtotal': item.subtotal
        })
    
    # Email context
    context = {
        'order_id': order.order_id,
        'customer_name': order.customer_name,
        'items': items_details,
        'total_amount': order.total_amount,
        'shipping_address': order.shipping_address,
        'shipping_city': order.shipping_city,
        'shipping_state': order.shipping_state,
        'shipping_pincode': order.shipping_pincode,
    }
    
    # Plain text message
    message = f"""
Dear {order.customer_name},

Thank you for your order!

Your order #{order.order_id} has been successfully placed and payment received.

Order Details:
"""
    for item in items_details:
        message += f"\n- {item['name']} x {item['quantity']} = ₹{item['subtotal']}"
    
    message += f"""

Total Amount: ₹{order.total_amount}

Shipping Address:
{order.shipping_address}
{order.shipping_city}, {order.shipping_state} - {order.shipping_pincode}

What's Next?
- Our team will contact you within 24-48 hours
- We'll start processing your order immediately
- You'll receive tracking information once shipped

If you have any questions, please contact us at info@printbox3d.com

Best regards,
PrintBox3D Team
"""
    
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"Attempting to send email to {order.customer_email}")
        logger.info(f"SMTP Config: {settings.EMAIL_HOST}:{settings.EMAIL_PORT}, TLS={settings.EMAIL_USE_TLS}, SSL={getattr(settings, 'EMAIL_USE_SSL', False)}")
        logger.info(f"From: {settings.DEFAULT_FROM_EMAIL}")
        
        # Send email to customer
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.customer_email],
            fail_silently=False,
        )
        
        logger.info(f"Email sent successfully to {order.customer_email}")
        
        # Send notification to admin
        send_order_notification_to_admin(order, items_details)
        
        return True
    except Exception as e:
        logger.error(f"Error sending order confirmation email: {e}", exc_info=True)
        return False


def send_order_notification_to_admin(order, items_details):
    """
    Send order notification email to admin/info email
    """
    subject = f'New Order Received - #{order.order_id}'
    
    message = f"""
New Order Received!

Order ID: {order.order_id}
Customer: {order.customer_name}
Email: {order.customer_email}
Phone: {order.customer_phone}

Order Items:
"""
    for item in items_details:
        message += f"\n- {item['name']} x {item['quantity']} = ₹{item['subtotal']}"
    
    message += f"""

Total Amount: ₹{order.total_amount}
Payment Status: {order.payment_status}

Shipping Address:
{order.shipping_address}
{order.shipping_city}, {order.shipping_state} - {order.shipping_pincode}

Action Required:
Please contact the customer within 24-48 hours to confirm the order.

View order details in the admin panel.
"""
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['info@printbox3d.com'],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending admin notification email: {e}")
        return False


def send_custom_order_notification(custom_order):
    """
    Send notification emails for custom order requests
    """
    # Email to customer
    customer_subject = 'Custom Order Request Received - PrintBox3D'
    customer_message = f"""
Dear {custom_order.name},

Thank you for your custom order request!

We have received your request and our team will review it carefully. We'll contact you within 24-48 hours with a quote and further details.

Request Details:
- Material: {custom_order.material}
- Color: {custom_order.color}
- Quantity: {custom_order.quantity}
- Budget: {custom_order.budget}

Description:
{custom_order.description}

If you have any immediate questions, please contact us at info@printbox3d.com

Best regards,
PrintBox3D Team
"""
    
    # Email to admin
    admin_subject = f'New Custom Order Request - #{custom_order.id}'
    admin_message = f"""
New Custom Order Request Received!

Request ID: #{custom_order.id}

Customer Details:
Name: {custom_order.name}
Email: {custom_order.email}
Phone: {custom_order.phone}

Order Details:
Material: {custom_order.material}
Color: {custom_order.color}
Quantity: {custom_order.quantity}
Budget: {custom_order.budget}

Description:
{custom_order.description}

Design File: {'Uploaded' if custom_order.design_file else 'Not uploaded'}

Action Required:
Please review the request and contact the customer within 24-48 hours.

View request details in the admin panel.
"""
    
    try:
        # Send to customer
        send_mail(
            subject=customer_subject,
            message=customer_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[custom_order.email],
            fail_silently=False,
        )
        
        # Send to admin
        send_mail(
            subject=admin_subject,
            message=admin_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['info@printbox3d.com'],
            fail_silently=False,
        )
        
        return True
    except Exception as e:
        print(f"Error sending custom order notification: {e}")
        return False


def send_contact_message_notification(contact_message):
    """
    Send notification for contact form submission
    """
    # Email to customer (acknowledgment)
    customer_subject = f'Message Received - PrintBox3D'
    customer_message = f"""
Dear {contact_message.name},

Thank you for contacting PrintBox3D!

We have received your message and will get back to you as soon as possible, usually within 24 hours.

Your Message:
Subject: {contact_message.subject}
{contact_message.message}

If you need immediate assistance, please call us or email info@printbox3d.com

Best regards,
PrintBox3D Team
"""
    
    # Email to admin
    admin_subject = f'New Contact Message - {contact_message.subject}'
    admin_message = f"""
New Contact Form Submission!

From: {contact_message.name}
Email: {contact_message.email}
Subject: {contact_message.subject}

Message:
{contact_message.message}

Please respond to the customer at: {contact_message.email}
"""
    
    try:
        # Send acknowledgment to customer
        send_mail(
            subject=customer_subject,
            message=customer_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[contact_message.email],
            fail_silently=False,
        )
        
        # Send notification to admin
        send_mail(
            subject=admin_subject,
            message=admin_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['info@printbox3d.com'],
            fail_silently=False,
        )
        
        return True
    except Exception as e:
        print(f"Error sending contact message notification: {e}")
        return False
