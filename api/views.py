"""
API Views for PrintBox3D E-commerce Platform

This module contains all API endpoints for the PrintBox3D application including:
- Product catalog management (categories, materials, products)
- Order creation and payment processing (Razorpay integration)
- Custom order requests
- Contact form submissions
- Newsletter subscriptions
- Customer testimonials
"""

from django.http import JsonResponse, HttpResponse
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import logging
import threading
import json

from .services.razorpay_service import RazorpayService
from .services.s3_service import S3Service
from .email_utils import (
    send_order_confirmation_email,
    send_custom_order_notification,
    send_contact_message_notification
)
from .models import (
    Category, Material, Product, CustomOrder,
    ContactMessage, Newsletter, Testimonial,
    Order, OrderItem, Payment, Coupon
)
from .serializers import (
    CategorySerializer, MaterialSerializer,
    ProductListSerializer, ProductDetailSerializer,
    CustomOrderSerializer, ContactMessageSerializer,
    NewsletterSerializer, TestimonialSerializer,
    OrderSerializer, PaymentSerializer, CreateOrderSerializer, CouponSerializer
)

logger = logging.getLogger(__name__)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for product categories.
    
    Provides read-only access to product categories.
    Categories are used to organize products (e.g., Home Decor, Accessories).
    
    Endpoints:
        GET /api/categories/ - List all categories
        GET /api/categories/{slug}/ - Get category by slug
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class MaterialViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for 3D printing materials.
    
    Provides read-only access to available printing materials.
    Materials define what products are made from (e.g., PLA, ABS, Resin).
    
    Endpoints:
        GET /api/materials/ - List all materials
        GET /api/materials/{id}/ - Get material by ID
    """
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for products with filtering and search capabilities.
    
    Provides read-only access to available products with advanced filtering,
    searching, and sorting options.
    
    Endpoints:
        GET /api/products/ - List all products
        GET /api/products/{slug}/ - Get product details by slug
        GET /api/products/featured/ - Get featured products (max 6)
        GET /api/products/best_sellers/ - Get best-selling products (max 6)
    
    Query Parameters:
        category__slug - Filter by category slug
        material__name - Filter by material name
        is_featured - Filter featured products (true/false)
        search - Search in name and description
        ordering - Sort by: price, name, created_at (prefix with - for descending)
    
    Examples:
        /api/products/?category__slug=home-decor
        /api/products/?search=keychain&ordering=-price
        /api/products/?is_featured=true
    """
    queryset = Product.objects.filter(is_available=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug', 'material__name', 'is_featured']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'name', 'created_at', 'is_featured']
    ordering = ['-is_featured', '-created_at']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        """Use detailed serializer for single product, list serializer for multiple."""
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """
        Get featured products.
        
        Returns up to 6 featured products for homepage display.
        """
        featured_products = self.queryset.filter(is_featured=True)[:6]
        serializer = self.get_serializer(featured_products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def best_sellers(self, request):
        """
        Get best-selling products.
        
        Currently returns featured products. Can be enhanced with actual sales data.
        """
        best_sellers = self.queryset.filter(is_featured=True)[:6]
        serializer = self.get_serializer(best_sellers, many=True)
        return Response(serializer.data)


class CustomOrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint for custom order requests.
    
    Allows customers to submit custom 3D printing requests with file uploads
    and specifications. Sends email notifications to admin.
    
    Endpoints:
        POST /api/custom-orders/ - Submit custom order request
    
    Request Body:
        name - Customer name
        email - Customer email
        phone - Customer phone number
        description - Order description
        file - 3D model file (optional)
    """
    queryset = CustomOrder.objects.all()
    serializer_class = CustomOrderSerializer
    http_method_names = ['post', 'get']
    
    def create(self, request, *args, **kwargs):
        """Create custom order and send notification email."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        custom_order = serializer.save()
        
        # Send email notification to admin
        try:
            send_custom_order_notification(custom_order)
        except Exception as email_error:
            logger.warning(f"Failed to send custom order notification: {email_error}")
        
        return Response({
            'message': 'Custom order request submitted successfully! We will contact you within 24-48 hours.',
            'order_id': serializer.data['id']
        }, status=status.HTTP_201_CREATED)


class ContactMessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for contact form submissions.
    
    Allows visitors to send messages through the contact form.
    Sends email notifications to admin.
    
    Endpoints:
        POST /api/contact/ - Submit contact message
    
    Request Body:
        name - Sender name
        email - Sender email
        subject - Message subject
        message - Message content
    """
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    http_method_names = ['post', 'get']
    
    def create(self, request, *args, **kwargs):
        """Create contact message and send notification email."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contact_message = serializer.save()
        
        # Send email notification to admin
        try:
            send_contact_message_notification(contact_message)
        except Exception as email_error:
            logger.warning(f"Failed to send contact message notification: {email_error}")
        
        return Response({
            'message': 'Thank you for contacting us! We will respond within 24 hours.',
            'message_id': serializer.data['id']
        }, status=status.HTTP_201_CREATED)


class NewsletterViewSet(viewsets.ModelViewSet):
    """
    API endpoint for newsletter subscriptions.
    
    Allows visitors to subscribe to email newsletter.
    
    Endpoints:
        POST /api/newsletter/ - Subscribe to newsletter
    
    Request Body:
        email - Subscriber email address
    """
    queryset = Newsletter.objects.filter(is_active=True)
    serializer_class = NewsletterSerializer
    http_method_names = ['post']
    
    def create(self, request, *args, **kwargs):
        """Subscribe user to newsletter."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response({
            'message': 'Successfully subscribed to our newsletter!',
            'email': serializer.data['email']
        }, status=status.HTTP_201_CREATED)


class TestimonialViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for customer testimonials.
    
    Provides read-only access to customer reviews and testimonials.
    
    Endpoints:
        GET /api/testimonials/ - List all testimonials
        GET /api/testimonials/featured/ - Get featured testimonials (max 6)
    """
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured testimonials for homepage display."""
        featured = self.queryset.filter(is_featured=True)[:6]
        serializer = self.get_serializer(featured, many=True)
        return Response(serializer.data)


# ============================================================================
# PAYMENT & ORDER PROCESSING
# ============================================================================

@api_view(['POST'])
@permission_classes([AllowAny])
def validate_coupon(request):
    """
    Validate a coupon code against the current cart total.

    Request Body:
        code        - The coupon code string
        cart_total  - Current cart total (numeric)

    Returns:
        valid           - true/false
        discount_amount - Amount discounted (if valid)
        message         - Error message (if invalid)
        coupon          - Coupon details (if valid)
    """
    from decimal import Decimal, InvalidOperation
    from django.utils import timezone

    code = request.data.get('code', '').strip().upper()
    cart_total_raw = request.data.get('cart_total', 0)

    if not code:
        return Response({'valid': False, 'message': 'Please enter a coupon code.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        cart_total = Decimal(str(cart_total_raw))
    except InvalidOperation:
        return Response({'valid': False, 'message': 'Invalid cart total.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        coupon = Coupon.objects.get(code=code, is_active=True)
    except Coupon.DoesNotExist:
        return Response({'valid': False, 'message': 'Invalid or expired coupon code.'})

    # Check expiry
    if coupon.expiry_date and coupon.expiry_date < timezone.now().date():
        return Response({'valid': False, 'message': 'This coupon has expired.'})

    # Check max uses
    if coupon.max_uses is not None and coupon.times_used >= coupon.max_uses:
        return Response({'valid': False, 'message': 'This coupon has reached its usage limit.'})

    # Check minimum order amount
    if cart_total < coupon.min_order_amount:
        return Response({
            'valid': False,
            'message': f'Minimum order amount of ₹{coupon.min_order_amount} required for this coupon.'
        })

    discount_amount = coupon.calculate_discount(cart_total)

    return Response({
        'valid': True,
        'discount_amount': str(discount_amount),
        'coupon': CouponSerializer(coupon).data,
        'message': f'Coupon applied! You save ₹{discount_amount}.'
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def create_order(request):
    """
    Create new order and initiate Razorpay payment.
    
    This endpoint:
    1. Validates order data and cart items
    2. Checks product availability and stock
    3. Creates Order and OrderItem records
    4. Initializes Razorpay payment order
    5. Returns payment details for frontend
    
    Request Body:
        customer_name - Customer full name
        customer_email - Customer email
        customer_phone - Customer phone number
        shipping_address - Delivery address
        shipping_city - Delivery city
        shipping_state - Delivery state
        shipping_pincode - Delivery PIN code
        items - Array of {product_id, quantity}
    
    Returns:
        order_id - Internal order ID
        razorpay_order_id - Razorpay order ID for payment
        razorpay_key_id - Razorpay public key
        amount - Payment amount in paise (₹ * 100)
        currency - Payment currency (INR)
        customer_* - Customer details for payment form
    
    Example Response:
        {
            "order_id": "ORD20251211123456ABCD",
            "razorpay_order_id": "order_XXX",
            "razorpay_key_id": "rzp_live_XXX",
            "amount": 29900,
            "currency": "INR",
            "customer_name": "John Doe",
            "customer_email": "john@example.com",
            "customer_phone": "9876543210"
        }
    """
    serializer = CreateOrderSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    
    # Calculate total amount from cart items
    total_amount = 0
    order_items = []
    
    for item in data['items']:
        try:
            product = Product.objects.get(id=item['product_id'], is_available=True)
            quantity = int(item['quantity'])
            
            # Check stock
            if product.stock_quantity < quantity:
                return Response({
                    'error': f'Insufficient stock for {product.name}. Available: {product.stock_quantity}'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            subtotal = product.price * quantity
            total_amount += subtotal
            
            order_items.append({
                'product': product,
                'product_name': product.name,
                'product_price': product.price,
                'product_image': product.image_url,
                'quantity': quantity,
                'subtotal': subtotal
            })
            
        except Product.DoesNotExist:
            return Response({
                'error': f'Product with ID {item["product_id"]} not found'
            }, status=status.HTTP_404_NOT_FOUND)
    
    # Apply coupon discount if provided
    coupon_code_input = data.get('coupon_code', '').strip().upper()
    discount_amount = 0
    applied_coupon = None

    if coupon_code_input:
        from decimal import Decimal
        from django.utils import timezone
        try:
            applied_coupon = Coupon.objects.get(code=coupon_code_input, is_active=True)
            # Re-validate before applying
            expired = applied_coupon.expiry_date and applied_coupon.expiry_date < timezone.now().date()
            maxed = applied_coupon.max_uses is not None and applied_coupon.times_used >= applied_coupon.max_uses
            below_min = total_amount < applied_coupon.min_order_amount
            if not expired and not maxed and not below_min:
                discount_amount = applied_coupon.calculate_discount(total_amount)
                total_amount = max(Decimal('0'), total_amount - discount_amount)
            else:
                applied_coupon = None  # invalid at this point, ignore silently
        except Coupon.DoesNotExist:
            pass  # invalid code, just ignore

    # Create order
    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        customer_name=data['customer_name'],
        customer_email=data['customer_email'],
        customer_phone=data['customer_phone'],
        shipping_address=data['shipping_address'],
        shipping_city=data['shipping_city'],
        shipping_state=data['shipping_state'],
        shipping_pincode=data['shipping_pincode'],
        total_amount=total_amount,
        discount_amount=discount_amount,
        coupon_code=applied_coupon.code if applied_coupon else '',
        status='PENDING',
        payment_status='PENDING'
    )

    # Create order items
    for item_data in order_items:
        product = item_data.pop('product')
        OrderItem.objects.create(order=order, product=product, **item_data)

    # Increment coupon usage after order is saved
    if applied_coupon:
        Coupon.objects.filter(pk=applied_coupon.pk).update(times_used=applied_coupon.times_used + 1)
    
    # Create Razorpay order via service layer
    try:
        rz_order = RazorpayService.create_order(
            amount_inr=float(total_amount),
            receipt=order.order_id,
            notes={'internal_order_id': order.order_id},
        )

        # Persist Razorpay order ID
        order.razorpay_order_id = rz_order['id']
        order.save(update_fields=['razorpay_order_id'])

        # Create payment record
        Payment.objects.create(
            order=order,
            razorpay_order_id=rz_order['id'],
            amount=total_amount,
            currency='INR',
            status='CREATED',
        )

        return Response({
            'order_id': order.order_id,
            'razorpay_order_id': rz_order['id'],
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'amount': rz_order['amount'],    # already in paise from service
            'currency': 'INR',
            'customer_name': order.customer_name,
            'customer_email': order.customer_email,
            'customer_phone': order.customer_phone,
        }, status=status.HTTP_201_CREATED)
        
    except ValueError as ve:
        # Razorpay credentials not configured
        order.delete()
        logger.error(f"Razorpay configuration error: {str(ve)}")
        return Response({
            'error': 'Payment gateway not configured',
            'details': 'Please contact support'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    except Exception as e:
        # Delete order if Razorpay order creation fails
        order.delete()
        logger.error(f"Razorpay order creation failed: {str(e)}", exc_info=True)
        return Response({
            'error': 'Failed to create payment order',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ============================================================================
# PAYMENT VERIFICATION (plain Django view - avoids DRF/CSRF middleware issues)
# ============================================================================
def verify_payment_simple(request):
    """
    Verify Razorpay payment signature. Uses plain Django view to avoid
    DRF middleware conflicts with CSRF-exempt payment callbacks.
    """
    logger.info(f"[VERIFY] Method: {request.method}")

    # Add CORS headers to response
    def add_cors(response):
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response['Access-Control-Allow-Credentials'] = 'true'
        return response
    
    # Handle OPTIONS preflight
    if request.method == 'OPTIONS':
        logger.info("[VERIFY_SIMPLE] Handling OPTIONS request")
        response = HttpResponse()
        return add_cors(response)
    
    # Only allow POST
    if request.method != 'POST':
        response = JsonResponse({'error': 'Method not allowed'}, status=405)
        return add_cors(response)
    
    try:
        import json
        data = json.loads(request.body)
        
        razorpay_order_id = data.get('razorpay_order_id', '').strip()
        razorpay_payment_id = data.get('razorpay_payment_id', '').strip()
        razorpay_signature  = data.get('razorpay_signature', '').strip()
        
        if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature]):
            response = JsonResponse({'success': False, 'error': 'Missing fields'}, status=400)
            return add_cors(response)
        
        # Find order
        try:
            order = Order.objects.get(razorpay_order_id=razorpay_order_id)
        except Order.DoesNotExist:
            response = JsonResponse({'success': False, 'error': 'Order not found'}, status=404)
            return add_cors(response)
        
        # Verify signature via service layer (HMAC-SHA256)
        if not RazorpayService.verify_signature(
            razorpay_order_id, razorpay_payment_id, razorpay_signature
        ):
            order.status = 'FAILED'
            order.payment_status = 'FAILED'
            order.save(update_fields=['status', 'payment_status'])
            response = JsonResponse({'success': False, 'error': 'Invalid signature'}, status=400)
            return add_cors(response)
        
        # Update order
        order.status = "PAID"
        order.payment_status = "CAPTURED"
        order.razorpay_payment_id = razorpay_payment_id
        order.save()
        
        # Send confirmation email in background thread (non-blocking)
        def send_email_async():
            try:
                send_order_confirmation_email(order)
                logger.info(f"Confirmation email sent for order {order.order_id}")
            except Exception as email_error:
                logger.error(f"Email sending error: {email_error}", exc_info=True)
        
        # daemon=False ensures the thread completes even after the response is returned
        email_thread = threading.Thread(target=send_email_async)
        email_thread.daemon = False
        email_thread.start()
        
        response = JsonResponse({
            'success': True,
            'order_id': order.order_id,
            'status': 'PAID'
        })
        return add_cors(response)
        
    except Exception as e:
        logger.error(f"Payment verification error: {e}", exc_info=True)
        response = JsonResponse({'success': False, 'error': str(e)}, status=500)
        return add_cors(response)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_order_status(request, order_id):
    """
    Get order status by order ID
    """
    try:
        order = Order.objects.get(order_id=order_id)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([AllowAny])
def payment_failed(request):
    """
    Handle payment failure
    """
    order_id = request.data.get('order_id')
    error_description = request.data.get('error_description', 'Payment failed')
    
    try:
        order = Order.objects.get(order_id=order_id)
        order.status = 'FAILED'
        order.payment_status = 'FAILED'
        order.save()
        
        if hasattr(order, 'payment'):
            payment = order.payment
            payment.status = 'FAILED'
            payment.error_description = error_description
            payment.save()
        
        return Response({
            'message': 'Payment failure recorded',
            'order_id': order.order_id
        }, status=status.HTTP_200_OK)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_orders(request):
    """
    Get all orders for the authenticated user
    Returns orders linked to user account + orders with matching email
    """
    # Get orders linked to user account
    user_orders = Order.objects.filter(user=request.user)
    
    # Also get orders with the same email (for guest checkouts before login)
    email_orders = Order.objects.filter(customer_email=request.user.email)
    
    # Combine and remove duplicates, order by creation date
    all_orders = (user_orders | email_orders).distinct().order_by('-created_at')
    
    serializer = OrderSerializer(all_orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# ============================================================================
# S3 PRESIGNED UPLOAD URL
# ============================================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_s3_upload_url(request):
    """
    Return a presigned S3 upload URL so the client can PUT a file directly to
    S3 without the file passing through Django.

    Body:
        folder      – destination folder in the bucket (default: 'products')
        file_name   – original filename (used to derive extension)
        content_type – MIME type of the file
        file_size   – size in bytes (used for validation)
    """
    if not S3Service.is_configured():
        return Response({'error': 'S3 storage is not configured'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    folder       = request.data.get('folder', 'products')
    file_name    = request.data.get('file_name', '')
    content_type = request.data.get('content_type', '')
    file_size    = int(request.data.get('file_size', 0))

    if not file_name or not content_type:
        return Response({'error': 'file_name and content_type are required'}, status=status.HTTP_400_BAD_REQUEST)

    # Validate MIME type and size
    type_ok, type_err = S3Service.validate_file_type(folder, content_type)
    if not type_ok:
        return Response({'error': type_err}, status=status.HTTP_400_BAD_REQUEST)

    size_ok, size_err = S3Service.validate_file_size(folder, file_size)
    if not size_ok:
        return Response({'error': size_err}, status=status.HTTP_400_BAD_REQUEST)

    result = S3Service.generate_presigned_upload_url(
        folder=folder,
        file_name=file_name,
        content_type=content_type,
    )
    if result is None:
        logger.error('S3Service failed to generate presigned URL')
        return Response({'error': 'Could not generate upload URL'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    upload_url, file_url, s3_key = result
    return Response({
        'upload_url': upload_url,
        'file_url':   file_url,
        's3_key':     s3_key,
    }, status=status.HTTP_200_OK)


# ============================================================================
# RAZORPAY WEBHOOK
# ============================================================================

@csrf_exempt
def razorpay_webhook(request):
    """
    Receives Razorpay event webhooks and reconciles payment / order status.
    Must be registered with CSRF exempt because Razorpay sends a raw POST.
    """
    if request.method != 'POST':
        return HttpResponse(status=405)

    raw_body   = request.body
    header_sig = request.headers.get('X-Razorpay-Signature', '')

    if not RazorpayService.verify_webhook_signature(raw_body, header_sig):
        logger.warning('Razorpay webhook: invalid signature')
        return HttpResponse(status=400)

    try:
        payload = json.loads(raw_body)
    except json.JSONDecodeError:
        return HttpResponse(status=400)

    event = payload.get('event', '')
    logger.info('Razorpay webhook received: %s', event)

    if event == 'payment.captured':
        rz_order_id  = payload['payload']['payment']['entity'].get('order_id', '')
        rz_payment_id = payload['payload']['payment']['entity'].get('id', '')
        try:
            order = Order.objects.get(razorpay_order_id=rz_order_id)
            if order.status not in ('CONFIRMED', 'SHIPPED', 'DELIVERED'):
                order.status         = 'CONFIRMED'
                order.payment_status = 'PAID'
                order.save(update_fields=['status', 'payment_status'])
                Payment.objects.filter(order=order).update(
                    status='CAPTURED', razorpay_payment_id=rz_payment_id
                )
        except Order.DoesNotExist:
            logger.error('Webhook: order not found for razorpay_order_id=%s', rz_order_id)

    elif event == 'payment.failed':
        rz_order_id = payload['payload']['payment']['entity'].get('order_id', '')
        try:
            order = Order.objects.get(razorpay_order_id=rz_order_id)
            if order.status not in ('CONFIRMED', 'SHIPPED', 'DELIVERED'):
                order.status         = 'FAILED'
                order.payment_status = 'FAILED'
                order.save(update_fields=['status', 'payment_status'])
                Payment.objects.filter(order=order).update(status='FAILED')
        except Order.DoesNotExist:
            logger.error('Webhook: order not found for razorpay_order_id=%s', rz_order_id)

    return HttpResponse(status=200)
