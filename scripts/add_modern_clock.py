"""
Add Modern Clock product to database with variant pricing info
"""
import os
import sys
import django

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'printbox_backend.settings')
django.setup()

from api.models import Product, Category, Material

def add_modern_clock():
    """Add or update the modern clock product"""
    
    # Get category and material
    try:
        home_decor = Category.objects.get(name='Home Decor')
        pla = Material.objects.get(name='PLA')
    except (Category.DoesNotExist, Material.DoesNotExist) as e:
        print(f"Error: {e}")
        print("Please ensure Home Decor category and PLA material exist")
        return
    
    # Update or create the clock product
    # Using base price for "without MagSafe" variant
    product, created = Product.objects.update_or_create(
        slug='modern-clock',
        defaults={
            'name': 'Modern Clock',
            'description': '''Premium 3D printed modern clock with sleek design. Features silent quartz movement for peaceful timekeeping.

Available in two variants:
• Without MagSafe Charger - ₹999
• With MagSafe Charger - ₹1,599

The MagSafe variant includes an integrated wireless charging pad compatible with iPhone 12 and newer models. Perfect blend of functionality and contemporary aesthetics.''',
            'category': home_decor,
            'material': pla,
            'price': 999.00,  # Base price (without MagSafe)
            'color': 'Black/White',
            'dimensions': '25cm x 15cm x 5cm',
            'weight': 300,
            'stock_quantity': 20,
            'is_featured': True,  # Make it featured
            'image': 'products/special-collections/modern-clock/modern-clock1.webp',
            'frontend_image': '/assets/products/special-collections/modern-clock/modern-clock1.webp'
        }
    )
    
    action = "Created" if created else "Updated"
    print(f"{action} product: {product.name}")
    print(f"  - Slug: {product.slug}")
    print(f"  - Base Price: ₹{product.price} (Without MagSafe)")
    print(f"  - MagSafe Variant: ₹1,599")
    print(f"  - Featured: {product.is_featured}")
    print(f"  - Image: {product.frontend_image}")
    print(f"  - Stock: {product.stock_quantity}")
    
    # Note about additional images
    print("\nNote: Additional images available at:")
    print("  - /assets/products/special-collections/modern-clock/modern-clock2.webp")
    print("  - /assets/products/special-collections/modern-clock/modern-clock3.webp")
    print("  - /assets/products/special-collections/modern-clock/modern-clock4.webp")
    print("\n⚠️  IMPORTANT: Frontend needs to be updated to handle variant selection")
    print("  Variants: Without MagSafe (₹999) | With MagSafe (₹1,599)")

if __name__ == '__main__':
    add_modern_clock()
    print("\n✓ Modern Clock product updated successfully!")
