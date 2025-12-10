from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.conf import settings
import razorpay
import hmac
import hashlib

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
import logging

logger = logging.getLogger(__name__)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing categories
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class MaterialViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing materials
    """
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing products with filtering and search
    """
    queryset = Product.objects.filter(is_available=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug', 'material__name', 'is_featured']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'name', 'created_at']
    ordering = ['-created_at']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured products"""
        featured_products = self.queryset.filter(is_featured=True)[:6]
        serializer = self.get_serializer(featured_products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def best_sellers(self, request):
        """Get best selling products (placeholder - can be enhanced with order data)"""
        best_sellers = self.queryset.filter(is_featured=True)[:6]
        serializer = self.get_serializer(best_sellers, many=True)
        return Response(serializer.data)


class CustomOrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for custom order submissions
    """
    queryset = CustomOrder.objects.all()
    serializer_class = CustomOrderSerializer
    http_method_names = ['post', 'get']  # Only allow POST to create, GET to list (admin only)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        custom_order = serializer.save()
        
        # Send email notifications
        try:
            send_custom_order_notification(custom_order)
        except Exception as email_error:
            print(f"Failed to send custom order notification: {email_error}")
        
        return Response({
            'message': 'Custom order request submitted successfully! We will contact you within 24-48 hours.',
            'order_id': serializer.data['id']
        }, status=status.HTTP_201_CREATED)


class ContactMessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for contact form submissions
    """
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    http_method_names = ['post', 'get']  # Only allow POST to create
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contact_message = serializer.save()
        
        # Send email notifications
        try:
            send_contact_message_notification(contact_message)
        except Exception as email_error:
            print(f"Failed to send contact message notification: {email_error}")
        
        return Response({
            'message': 'Thank you for contacting us! We will get back to you soon.',
            'id': serializer.data['id']
        }, status=status.HTTP_201_CREATED)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response({
            'message': 'Thank you for contacting us! We will respond within 24 hours.',
            'message_id': serializer.data['id']
        }, status=status.HTTP_201_CREATED)


class NewsletterViewSet(viewsets.ModelViewSet):
    """
    ViewSet for newsletter subscriptions
    """
    queryset = Newsletter.objects.filter(is_active=True)
    serializer_class = NewsletterSerializer
    http_method_names = ['post']  # Only allow POST to subscribe
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response({
            'message': 'Successfully subscribed to our newsletter!',
            'email': serializer.data['email']
        }, status=status.HTTP_201_CREATED)


class TestimonialViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing testimonials
    """
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured testimonials"""
        featured = self.queryset.filter(is_featured=True)[:6]
        serializer = self.get_serializer(featured, many=True)
        return Response(serializer.data)


# Initialize Razorpay client
def get_razorpay_client():
    """Get Razorpay client with error handling"""
    if not settings.RAZORPAY_KEY_ID or not settings.RAZORPAY_KEY_SECRET:
        logger.error("Razorpay credentials not configured in environment variables")
        raise ValueError("Razorpay credentials not configured")
    
    return razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@api_view(['POST'])
@permission_classes([AllowAny])
def create_order(request):
    """
    Create a new order and initiate Razorpay payment
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


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_payment(request):
    """
    Verify Razorpay payment signature and update order status
    """
    serializer = PaymentVerificationSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    
    try:
        order = Order.objects.get(order_id=data['order_id'])
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Verify signature
    try:
        # Create signature
        generated_signature = hmac.new(
            settings.RAZORPAY_KEY_SECRET.encode(),
            f"{data['razorpay_order_id']}|{data['razorpay_payment_id']}".encode(),
            hashlib.sha256
        ).hexdigest()
        
        if generated_signature == data['razorpay_signature']:
            # Payment verified successfully
            order.razorpay_payment_id = data['razorpay_payment_id']
            order.razorpay_signature = data['razorpay_signature']
            order.status = 'PAID'
            order.payment_status = 'CAPTURED'
            order.save()
            
            # Update payment record
            payment = order.payment
            payment.razorpay_payment_id = data['razorpay_payment_id']
            payment.razorpay_signature = data['razorpay_signature']
            payment.status = 'CAPTURED'
            payment.save()
            
            # Update product stock
            for item in order.items.all():
                if item.product:
                    item.product.stock_quantity -= item.quantity
                    item.product.save()
            
            # Send order confirmation emails
            try:
                send_order_confirmation_email(order)
            except Exception as email_error:
                print(f"Failed to send order confirmation email: {email_error}")
            
            return Response({
                'message': 'Payment verified successfully',
                'order_id': order.order_id,
                'status': 'PAID'
            }, status=status.HTTP_200_OK)
        else:
            # Signature verification failed
            order.status = 'FAILED'
            order.payment_status = 'FAILED'
            order.save()
            
            payment = order.payment
            payment.status = 'FAILED'
            payment.error_description = 'Signature verification failed'
            payment.save()
            
            return Response({
                'error': 'Payment verification failed'
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'error': 'Payment verification error',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
