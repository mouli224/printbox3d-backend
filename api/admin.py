from django.contrib import admin
from .models import (
    Category, Material, Product, CustomOrder,
    ContactMessage, Newsletter, Testimonial,
    Order, OrderItem, Payment, Coupon
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'image_url', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Image', {
            'fields': ('image_url', 'image'),
            'description': 'Preferred: paste a full S3 URL in "Image url". File upload (Image) is kept for legacy use.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name', 'description']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'material', 'price', 'stock_quantity', 'is_available', 'is_featured', 'created_at']
    list_filter = ['category', 'material', 'is_available', 'is_featured']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_available', 'is_featured', 'price']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'category', 'material')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock_quantity', 'is_available', 'is_featured')
        }),
        ('Product Details', {
            'fields': ('color', 'dimensions', 'weight')
        }),
        ('Images', {
            'fields': ('image_url', 'image_url_2', 'image_url_3'),
            'description': 'Paste the full S3 URL for each image (e.g. https://printbox-media.s3.ap-south-1.amazonaws.com/products/my-product.jpg)'
        }),
        ('SEO', {
            'fields': ('meta_description',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CustomOrder)
class CustomOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'phone', 'material', 'status', 'quantity', 'created_at']
    list_filter = ['status', 'material', 'created_at']
    search_fields = ['name', 'email', 'phone', 'description']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Order Details', {
            'fields': ('material', 'color', 'quantity', 'budget', 'description', 'design_file')
        }),
        ('Order Management', {
            'fields': ('status', 'quote_amount', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_delete_permission(self, request, obj=None):
        # Only allow deletion for cancelled orders
        if obj and obj.status not in ['CANCELLED', 'PENDING']:
            return False
        return True


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = ['is_read']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Message Details', {
            'fields': ('name', 'email', 'subject', 'message', 'is_read')
        }),
        ('Admin Notes', {
            'fields': ('admin_notes',)
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'subscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email']
    list_editable = ['is_active']
    readonly_fields = ['subscribed_at']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'rating', 'is_featured', 'created_at']
    list_filter = ['rating', 'is_featured', 'created_at']
    search_fields = ['name', 'company', 'message']
    list_editable = ['is_featured']
    readonly_fields = ['created_at']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'product_name', 'product_price', 'product_image', 'quantity', 'subtotal']
    can_delete = False


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_type', 'discount_value', 'min_order_amount', 'max_uses', 'times_used', 'is_active', 'expiry_date', 'created_at']
    list_filter = ['discount_type', 'is_active', 'created_at']
    search_fields = ['code']
    list_editable = ['is_active']
    readonly_fields = ['times_used', 'created_at']

    fieldsets = (
        ('Coupon Code', {
            'fields': ('code', 'is_active')
        }),
        ('Discount', {
            'fields': ('discount_type', 'discount_value', 'max_discount_amount')
        }),
        ('Restrictions', {
            'fields': ('min_order_amount', 'max_uses', 'expiry_date')
        }),
        ('Usage', {
            'fields': ('times_used', 'created_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'customer_name', 'customer_email', 'total_amount', 'status', 'payment_status', 'created_at']
    list_filter = ['status', 'payment_status', 'created_at']
    search_fields = ['order_id', 'customer_name', 'customer_email', 'customer_phone', 'razorpay_order_id', 'razorpay_payment_id']
    list_editable = ['status']
    readonly_fields = ['order_id', 'razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_id', 'status', 'payment_status', 'total_amount', 'discount_amount', 'coupon_code')
        }),
        ('Customer Details', {
            'fields': ('customer_name', 'customer_email', 'customer_phone')
        }),
        ('Shipping Address', {
            'fields': ('shipping_address', 'shipping_city', 'shipping_state', 'shipping_pincode')
        }),
        ('Payment Information', {
            'fields': ('razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature')
        }),
        ('Fulfillment', {
            'fields': ('tracking_number', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Orders should only be created through the API
        return False


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['razorpay_order_id', 'order', 'amount', 'currency', 'status', 'payment_method', 'created_at']
    list_filter = ['status', 'currency', 'created_at']
    search_fields = ['razorpay_order_id', 'razorpay_payment_id', 'order__order_id', 'order__customer_email']
    readonly_fields = ['order', 'razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature', 'amount', 'currency', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Payment Information', {
            'fields': ('order', 'razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature')
        }),
        ('Amount Details', {
            'fields': ('amount', 'currency', 'status', 'payment_method')
        }),
        ('Error Information', {
            'fields': ('error_code', 'error_description'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Payments should only be created through the API
        return False
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of payment records
        return False
