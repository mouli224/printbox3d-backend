from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify


class Category(models.Model):
    """Product categories like Home Decor, Gadgets, etc."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, help_text='Category image — paste the full S3 URL here (preferred over file upload)')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Material(models.Model):
    """3D Printing materials like PLA, ABS, PETG"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    properties = models.TextField(blank=True, help_text="Material properties and characteristics")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    """Products available in the shop"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)], help_text="Original price before discount")
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0), MaxValueValidator(100)], help_text="Discount percentage (0-100)")
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, related_name='products')
    
    # Product details
    color = models.CharField(max_length=50, blank=True)
    dimensions = models.CharField(max_length=100, blank=True, help_text="e.g., 12cm x 12cm x 10cm")
    weight = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, help_text="Weight in grams")
    
    # Images — store S3 URLs directly (paste from AWS S3 console or copied after upload)
    image_url   = models.URLField(max_length=500, blank=True, help_text='Primary image — paste the full S3 URL here')
    image_url_2 = models.URLField(max_length=500, blank=True, help_text='Second image URL (optional)')
    image_url_3 = models.URLField(max_length=500, blank=True, help_text='Third image URL (optional)')
    
    # Stock and availability
    stock_quantity = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    # SEO
    meta_description = models.TextField(blank=True, max_length=160)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class CustomOrder(models.Model):
    """Custom order requests from customers"""
    
    MATERIAL_CHOICES = [
        ('PLA', 'PLA - Standard'),
        ('ABS', 'ABS - Durable'),
        ('PETG', 'PETG - Strong & Flexible'),
        ('TPU', 'TPU - Flexible'),
        ('NYLON', 'Nylon - Industrial'),
        ('OTHER', 'Other (specify in notes)'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending Review'),
        ('REVIEWING', 'Under Review'),
        ('QUOTED', 'Quote Sent'),
        ('APPROVED', 'Approved'),
        ('IN_PRODUCTION', 'In Production'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    # Customer information
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # Order details
    material = models.CharField(max_length=20, choices=MATERIAL_CHOICES, default='PLA')
    color = models.CharField(max_length=50)
    description = models.TextField(help_text="Detailed description of the custom order")
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    budget = models.CharField(max_length=50, blank=True, help_text="Customer's budget range")
    
    # File upload
    design_file = models.FileField(
        upload_to='custom_orders/',
        blank=True,
        null=True,
        help_text="STL, OBJ, 3MF, STEP, or image files"
    )
    
    # Order management
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    admin_notes = models.TextField(blank=True, help_text="Internal notes (not visible to customer)")
    quote_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Quoted price for the custom order"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Custom Order #{self.id} - {self.name}"


class ContactMessage(models.Model):
    """Contact form submissions"""
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    
    is_read = models.BooleanField(default=False)
    admin_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"


class Newsletter(models.Model):
    """Newsletter subscriptions"""
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email


class Testimonial(models.Model):
    """Customer testimonials"""
    name = models.CharField(max_length=200)
    company = models.CharField(max_length=200, blank=True)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5
    )
    message = models.TextField()
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Testimonial from {self.name}"


class Order(models.Model):
    """Customer orders"""
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending Payment'),
        ('PAID', 'Payment Successful'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
        ('FAILED', 'Payment Failed'),
    ]
    
    # Order identification
    order_id = models.CharField(max_length=100, unique=True, editable=False)
    
    # User association (optional - for logged in users)
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    
    # Customer information
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    
    # Shipping address
    shipping_address = models.TextField()
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_pincode = models.CharField(max_length=20)
    
    # Order details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    # Payment tracking
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=200, blank=True, null=True)
    payment_status = models.CharField(max_length=20, default='PENDING')
    
    # Tracking
    tracking_number = models.CharField(max_length=100, blank=True)
    admin_notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at'], name='order_status_created_idx'),
        ]

    def save(self, *args, **kwargs):
        if not self.order_id:
            # Generate unique order ID
            import random
            import string
            from django.utils import timezone
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            self.order_id = f"ORD{timestamp}{random_str}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_id} - {self.customer_name}"


class OrderItem(models.Model):
    """Items in an order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    
    # Product snapshot (in case product is deleted/modified later)
    product_name = models.CharField(max_length=200)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_image = models.CharField(max_length=500, blank=True)
    
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"


class Payment(models.Model):
    """Payment transactions"""
    
    STATUS_CHOICES = [
        ('CREATED', 'Created'),
        ('AUTHORIZED', 'Authorized'),
        ('CAPTURED', 'Captured'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    ]
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    
    # Razorpay details
    razorpay_order_id = models.CharField(max_length=100)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=200, blank=True, null=True)
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='INR')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='CREATED')
    
    # Additional payment info
    payment_method = models.CharField(max_length=50, blank=True)
    error_code = models.CharField(max_length=100, blank=True)
    error_description = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment for {self.order.order_id} - {self.status}"
