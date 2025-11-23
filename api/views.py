from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .models import (
    Category, Material, Product, CustomOrder,
    ContactMessage, Newsletter, Testimonial
)
from .serializers import (
    CategorySerializer, MaterialSerializer,
    ProductListSerializer, ProductDetailSerializer,
    CustomOrderSerializer, ContactMessageSerializer,
    NewsletterSerializer, TestimonialSerializer
)


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
        self.perform_create(serializer)
        
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
