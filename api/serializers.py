from rest_framework import serializers
from .models import (
    Category, Material, Product, CustomOrder,
    ContactMessage, Newsletter, Testimonial,
    Order, OrderItem, Payment
)


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image', 'product_count', 'created_at']
    
    def get_product_count(self, obj):
        return obj.products.filter(is_available=True).count()


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'name', 'description', 'properties']


class ProductListSerializer(serializers.ModelSerializer):
    """Simplified serializer for product lists"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    material_name = serializers.CharField(source='material.name', read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'price', 'original_price', 'discount_percentage', 
            'image', 'frontend_image', 'category_name', 'material_name', 
            'is_featured', 'is_available', 'stock_quantity'
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for single product view"""
    category = CategorySerializer(read_only=True)
    material = MaterialSerializer(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price', 'original_price', 
            'discount_percentage', 'category', 'material', 'color', 'dimensions', 
            'weight', 'image', 'image_2', 'image_3', 'frontend_image', 
            'stock_quantity', 'is_available', 'is_featured', 'meta_description', 
            'created_at', 'updated_at'
        ]


class CustomOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomOrder
        fields = [
            'id', 'name', 'email', 'phone', 'material', 'color',
            'description', 'quantity', 'budget', 'design_file',
            'status', 'created_at'
        ]
        read_only_fields = ['status', 'created_at']
    
    def validate_design_file(self, value):
        """Validate file size and type"""
        if value:
            # Max file size: 10MB
            if value.size > 10 * 1024 * 1024:
                raise serializers.ValidationError("File size cannot exceed 10MB")
            
            # Allowed extensions
            allowed_extensions = ['.stl', '.obj', '.3mf', '.step', '.stp', '.jpg', '.jpeg', '.png', '.pdf']
            file_ext = value.name.lower().split('.')[-1]
            if f".{file_ext}" not in allowed_extensions:
                raise serializers.ValidationError(
                    f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
                )
        return value


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'subject', 'message', 'created_at']
        read_only_fields = ['created_at']


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ['id', 'email', 'subscribed_at']
        read_only_fields = ['subscribed_at']
    
    def validate_email(self, value):
        """Check if email already exists"""
        if Newsletter.objects.filter(email=value, is_active=True).exists():
            raise serializers.ValidationError("This email is already subscribed to our newsletter.")
        return value


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ['id', 'name', 'company', 'rating', 'message', 'image', 'created_at']


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for order items"""
    product_slug = serializers.CharField(source='product.slug', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'product_price', 'product_image', 'product_slug', 'quantity', 'subtotal']
        read_only_fields = ['id']


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for creating and viewing orders"""
    items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_id', 'customer_name', 'customer_email', 'customer_phone',
            'shipping_address', 'shipping_city', 'shipping_state', 'shipping_pincode',
            'status', 'total_amount', 'payment_status', 'tracking_number',
            'items', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'order_id', 'status', 'payment_status', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        
        return order


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for payment details"""
    order_id = serializers.CharField(source='order.order_id', read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id', 'order_id', 'razorpay_order_id', 'razorpay_payment_id',
            'amount', 'currency', 'status', 'payment_method',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'order_id', 'created_at', 'updated_at']


class CreateOrderSerializer(serializers.Serializer):
    """Serializer for creating a new order with items"""
    customer_name = serializers.CharField(max_length=200)
    customer_email = serializers.EmailField()
    customer_phone = serializers.CharField(max_length=20)
    shipping_address = serializers.CharField()
    shipping_city = serializers.CharField(max_length=100)
    shipping_state = serializers.CharField(max_length=100)
    shipping_pincode = serializers.CharField(max_length=20)
    items = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )
    
    def validate_items(self, value):
        """Validate cart items"""
        if not value:
            raise serializers.ValidationError("Cart cannot be empty")
        
        for item in value:
            if 'product_id' not in item or 'quantity' not in item:
                raise serializers.ValidationError("Each item must have product_id and quantity")
            
            try:
                quantity = int(item['quantity'])
                if quantity < 1:
                    raise serializers.ValidationError("Quantity must be at least 1")
            except (ValueError, TypeError):
                raise serializers.ValidationError("Invalid quantity value")
        
        return value


class PaymentVerificationSerializer(serializers.Serializer):
    """Serializer for verifying Razorpay payment"""
    razorpay_order_id = serializers.CharField()
    razorpay_payment_id = serializers.CharField()
    razorpay_signature = serializers.CharField()
    order_id = serializers.CharField()
