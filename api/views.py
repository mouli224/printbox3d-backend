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

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import razorpay
import hmac
import hashlib
import logging

from .email_utils import (
    send_order_confirmation_email,
    send_custom_order_notification,
    send_contact_message_notification
)

from .models import (
    Category, Material, Product, CustomOrder,
    ContactMessage, Newsletter, Testimonial,
    Order, OrderItem, Payment
)
from .serializers import (
    CategorySerializer, MaterialSerializer,
    ProductListSerializer, ProductDetailSerializer,
    CustomOrderSerializer, ContactMessageSerializer,
    NewsletterSerializer, TestimonialSerializer,
    OrderSerializer, PaymentSerializer, CreateOrderSerializer,
    PaymentVerificationSerializer
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
    ordering_fields = ['price', 'name', 'created_at']
    ordering = ['-created_at']
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

def get_razorpay_client():
    """
    Initialize and return Razorpay client.
    
    Returns:
        razorpay.Client: Configured Razorpay client instance
        
    Raises:
        ValueError: If Razorpay credentials are not configured
    """
    if not settings.RAZORPAY_KEY_ID or not settings.RAZORPAY_KEY_SECRET:
        logger.error("Razorpay credentials not configured in environment variables")
        raise ValueError("Razorpay credentials not configured")
    
    return razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

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
                'product_image': request.build_absolute_uri(product.image.url) if product.image else '',
                'quantity': quantity,
                'subtotal': subtotal
            })
            
        except Product.DoesNotExist:
            return Response({
                'error': f'Product with ID {item["product_id"]} not found'
            }, status=status.HTTP_404_NOT_FOUND)
    
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
        status='PENDING',
        payment_status='PENDING'
    )
    
    # Create order items
    for item_data in order_items:
        product = item_data.pop('product')
        OrderItem.objects.create(order=order, product=product, **item_data)
    
    # Create Razorpay order
    try:
        # Get Razorpay client
        razorpay_client = get_razorpay_client()
        
        razorpay_order = razorpay_client.order.create({
            'amount': int(total_amount * 100),  # Amount in paise
            'currency': 'INR',
            'receipt': order.order_id,
            'payment_capture': 1  # Auto capture payment
        })
        
        # Save Razorpay order ID
        order.razorpay_order_id = razorpay_order['id']
        order.save()
        
        # Create payment record
        Payment.objects.create(
            order=order,
            razorpay_order_id=razorpay_order['id'],
            amount=total_amount,
            currency='INR',
            status='CREATED'
        )
        
        return Response({
            'order_id': order.order_id,
            'razorpay_order_id': razorpay_order['id'],
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'amount': int(total_amount * 100),
            'currency': 'INR',
            'customer_name': order.customer_name,
            'customer_email': order.customer_email,
            'customer_phone': order.customer_phone
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


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def verify_payment(request):
    logger.info(f"Payment verification request received: {request.data}")

    try:
        # Extract fields safely
        razorpay_order_id = request.data.get("razorpay_order_id")
        razorpay_payment_id = request.data.get("razorpay_payment_id")
        razorpay_signature = request.data.get("razorpay_signature")

        if not (razorpay_order_id and razorpay_payment_id and razorpay_signature):
            return Response(
                {"error": "Missing required Razorpay fields"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Find order using Razorpay Order ID (THIS IS THE CORRECT METHOD)
        order = Order.objects.filter(razorpay_order_id=razorpay_order_id).first()

        if not order:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        logger.info(f"Order found: {order.order_id}")

        # Generate signature manually
        generated_signature = hmac.new(
            settings.RAZORPAY_KEY_SECRET.encode(),
            f"{razorpay_order_id}|{razorpay_payment_id}".encode(),
            hashlib.sha256
        ).hexdigest()

        logger.info(f"Generated: {generated_signature}")
        logger.info(f"Received: {razorpay_signature}")

        if generated_signature != razorpay_signature:
            # Mismatch
            order.status = "FAILED"
            order.payment_status = "FAILED"
            order.save(update_fields=["status", "payment_status"])

            payment = getattr(order, "payment", None)
            if payment:
                payment.status = "FAILED"
                payment.error_description = "Signature mismatch"
                payment.save()

            return Response(
                {"success": False, "error": "Signature verification failed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # SUCCESS
        order.status = "PAID"
        order.payment_status = "CAPTURED"
        order.razorpay_payment_id = razorpay_payment_id
        order.razorpay_signature = razorpay_signature
        order.save(update_fields=["status", "payment_status", "razorpay_payment_id", "razorpay_signature"])

        # Update payment record safely
        payment = getattr(order, "payment", None)
        if payment:
            payment.status = "CAPTURED"
            payment.razorpay_payment_id = razorpay_payment_id
            payment.razorpay_signature = razorpay_signature
            payment.save()

        # Reduce stock safely
        for item in order.items.all():
            if item.product:
                item.product.stock_quantity -= item.quantity
                item.product.save(update_fields=["stock_quantity"])

        # Send confirmation email
        try:
            send_order_confirmation_email(order)
        except Exception as e:
            logger.error(f"Email error: {e}")

        return Response(
            {"success": True, "order_id": order.order_id, "status": "PAID"},
            status=status.HTTP_200_OK
        )

    except Exception as e:
        logger.error(f"Payment verify crash: {str(e)}", exc_info=True)
        return Response(
            {"success": False, "error": "Server error", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )



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

@api_view(["GET"])
def debug_settings(request):
    from django.conf import settings
    return Response({
        "allowed_hosts": settings.ALLOWED_HOSTS,
        "cors_allowed": getattr(settings, "CORS_ALLOWED_ORIGINS", "NOT FOUND"),
        "cors_all": getattr(settings, "CORS_ALLOW_ALL_ORIGINS", "NOT FOUND"),
        "debug": settings.DEBUG,
        "cors_middleware": "corsheaders.middleware.CorsMiddleware" in settings.MIDDLEWARE
    })
