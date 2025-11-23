from rest_framework import serializers
from .models import (
    Category, Material, Product, CustomOrder,
    ContactMessage, Newsletter, Testimonial
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
            'id', 'name', 'slug', 'price', 'image', 'category_name',
            'material_name', 'is_featured', 'is_available', 'stock_quantity'
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for single product view"""
    category = CategorySerializer(read_only=True)
    material = MaterialSerializer(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price', 'category', 'material',
            'color', 'dimensions', 'weight', 'image', 'image_2', 'image_3',
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
