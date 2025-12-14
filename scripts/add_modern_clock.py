"""
Add Modern Clock product to database with multiple images
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
    product, created = Product.objects.update_or_create(
        slug='clock',
        defaults={
            'name': 'Modern Wall Clock',
            'description': 'Premium 3D printed modern wall clock with sleek geometric design. Features silent quartz movement for peaceful timekeeping. Perfect blend of functionality and contemporary aesthetics. Available in multiple color options to match any interior decor.',
            'category': home_decor,
            'material': pla,
            'price': 1099.00,
            'original_price': 1499.00,  # Add original price for discount
            'discount_percentage': 27,  # Calculate: (1499-1099)/1499 * 100
            'color': 'Black/White',
            'dimensions': '30cm x 30cm x 5cm',
            'weight': 350,
            'stock_quantity': 15,
            'is_featured': True,  # Make it featured
            'image': 'products/special-collections/clock/modern-clock1.JPG',
            'frontend_image': '/assets/products/special-collections/clock/modern-clock1.JPG'
        }
    )
    
    action = "Created" if created else "Updated"
    print(f"{action} product: {product.name}")
    print(f"  - Slug: {product.slug}")
    print(f"  - Price: ₹{product.price}")
    print(f"  - Discount: {product.discount_percentage}%")
    print(f"  - Featured: {product.is_featured}")
    print(f"  - Image: {product.frontend_image}")
    print(f"  - Stock: {product.stock_quantity}")
    
    # Note about additional images
    print("\nNote: Additional images available at:")
    print("  - /assets/products/special-collections/clock/modern-clock2.JPG")
    print("  - /assets/products/special-collections/clock/modern-clock3.JPG")
    print("  - /assets/products/special-collections/clock/modern-clock4.JPG")
    print("\nThese can be added to the product detail page gallery.")

if __name__ == '__main__':
    add_modern_clock()
    print("\n✓ Modern Clock product added successfully!")
