from django.contrib import admin
from .models import (
    Category, Material, Product, CustomOrder,
    ContactMessage, Newsletter, Testimonial
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']


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
            'fields': ('image', 'image_2', 'image_3')
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
