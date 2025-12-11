"""
Script to add new products from updated catalog
Run: python add_new_products.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'printbox_backend.settings')
django.setup()

from api.models import Product, Category, Material
from decimal import Decimal

# New product data (weight estimated in kg)
products_data = [
    # LAMPS (Featured Category)
    {'name': 'Ocean Drift Lamp', 'slug': 'ocean-drift-lamp', 'category': 'Lamps', 'material': 'PLA', 'price': 699, 'description': 'Modern ocean wave design lamp with LED lighting. Creates a soothing ambiance with its flowing pattern.', 'color': 'Blue/White/Transparent', 'dimensions': '20cm x 15cm x 15cm', 'weight': 0.20, 'stock_quantity': 15, 'is_featured': True, 'is_available': True},
    {'name': 'Tide Form Lamp', 'slug': 'tide-form-lamp', 'category': 'Lamps', 'material': 'PLA', 'price': 1299, 'description': 'Premium tide-inspired lamp with elegant curves. Features warm LED illumination.', 'color': 'White/Blue/Custom', 'dimensions': '25cm x 20cm x 18cm', 'weight': 0.30, 'stock_quantity': 10, 'is_featured': True, 'is_available': True},
    {'name': 'Reindeer Lamp Set', 'slug': 'reindeer-lamp-set', 'category': 'Lamps', 'material': 'PLA', 'price': 599, 'description': 'Festive reindeer lamp set perfect for Christmas decor. Includes LED lights.', 'color': 'White/Brown/Multi-color', 'dimensions': '18cm x 12cm x 15cm', 'weight': 0.18, 'stock_quantity': 20, 'is_featured': True, 'is_available': True},
    {'name': 'Christmas Tree Lamp', 'slug': 'christmas-tree-lamp', 'category': 'Lamps', 'material': 'PLA', 'price': 799, 'description': 'Beautiful Christmas tree lamp with integrated LED lights. Perfect holiday decoration.', 'color': 'Green/White/Multi-color', 'dimensions': '22cm x 15cm x 15cm', 'weight': 0.22, 'stock_quantity': 18, 'is_featured': True, 'is_available': True},
    {'name': 'Round Christmas Lamp', 'slug': 'round-christmas-lamp', 'category': 'Lamps', 'material': 'PLA', 'price': 699, 'description': 'Spherical Christmas-themed lamp with festive patterns. Warm LED glow.', 'color': 'Red/White/Gold', 'dimensions': '20cm diameter', 'weight': 0.20, 'stock_quantity': 15, 'is_featured': True, 'is_available': True},
    
    # KEYCHAINS (Featured Category)
    {'name': 'Spotify Keychain', 'slug': 'spotify-keychain', 'category': 'Keychains', 'material': 'PLA', 'price': 199, 'description': 'Custom Spotify code keychain with your favorite song. Scannable design.', 'color': 'Black/White/Green', 'dimensions': '8cm x 3cm x 0.5cm', 'weight': 0.015, 'stock_quantity': 50, 'is_featured': True, 'is_available': True},
    {'name': 'Custom Number Plate Keychain', 'slug': 'number-plate-keychain', 'category': 'Keychains', 'material': 'PLA', 'price': 199, 'description': 'Personalized vehicle number plate keychain. Perfect for car enthusiasts.', 'color': 'All Colors Available', 'dimensions': '9cm x 4cm x 0.5cm', 'weight': 0.018, 'stock_quantity': 60, 'is_featured': True, 'is_available': True},
    {'name': 'Octopus Keychain', 'slug': 'octopus-keychain-new', 'category': 'Keychains', 'material': 'PLA', 'price': 199, 'description': 'Cute octopus design keychain with detailed tentacles. Fun and unique.', 'color': 'Blue/Pink/Orange', 'dimensions': '6cm x 6cm x 4cm', 'weight': 0.020, 'stock_quantity': 45, 'is_featured': True, 'is_available': True},
    {'name': 'Gym Weight Keychain', 'slug': 'gym-weight-keychain', 'category': 'Keychains', 'material': 'PLA', 'price': 199, 'description': 'Miniature gym weight plate keychain for fitness lovers.', 'color': 'Black/Red/Silver', 'dimensions': '5cm diameter', 'weight': 0.015, 'stock_quantity': 40, 'is_featured': True, 'is_available': True},
    {'name': 'Dumbbell Keychain', 'slug': 'dumbbell-keychain', 'category': 'Keychains', 'material': 'PLA', 'price': 199, 'description': 'Realistic dumbbell keychain. Perfect gift for gym enthusiasts.', 'color': 'Black/Silver/Custom', 'dimensions': '7cm x 2.5cm x 2.5cm', 'weight': 0.018, 'stock_quantity': 40, 'is_featured': True, 'is_available': True},
    {'name': 'Mobile Stand Keychain', 'slug': 'mobile-stand-keychain', 'category': 'Keychains', 'material': 'PLA', 'price': 299, 'description': 'Functional keychain that doubles as a portable phone stand. Clever design.', 'color': 'Black/White/Custom', 'dimensions': '8cm x 5cm x 1cm', 'weight': 0.025, 'stock_quantity': 30, 'is_featured': True, 'is_available': True},
    {'name': 'Engine Keychain', 'slug': 'engine-keychain', 'category': 'Keychains', 'material': 'PLA', 'price': 299, 'description': 'Detailed miniature engine keychain for automobile enthusiasts.', 'color': 'Silver/Black/Custom', 'dimensions': '7cm x 5cm x 5cm', 'weight': 0.030, 'stock_quantity': 25, 'is_featured': True, 'is_available': True},
    {'name': 'XOX Game Keychain', 'slug': 'xox-game-keychain', 'category': 'Keychains', 'material': 'PLA', 'price': 299, 'description': 'Playable Tic-Tac-Toe keychain game. Fun and interactive accessory.', 'color': 'Multi-color/Custom', 'dimensions': '8cm x 8cm x 1.5cm', 'weight': 0.028, 'stock_quantity': 35, 'is_featured': True, 'is_available': True},
    {'name': 'Bag Zipper Tag Keychain', 'slug': 'zipper-tag-keychain', 'category': 'Keychains', 'material': 'PLA', 'price': 199, 'description': 'Custom bag zipper tag keychain. Personalize with your name or initials.', 'color': 'All Colors Available', 'dimensions': '6cm x 3cm x 0.5cm', 'weight': 0.012, 'stock_quantity': 50, 'is_featured': True, 'is_available': True},
    
    # TECH GADGETS
    {'name': 'Gear Shape Mobile Holder', 'slug': 'gear-mobile-holder', 'category': 'Tech Gadgets', 'material': 'PLA', 'price': 599, 'description': 'Industrial-style gear-shaped mobile holder. Rotating mechanism for angle adjustment.', 'color': 'Black/Silver/Gold', 'dimensions': '15cm x 12cm x 10cm', 'weight': 0.15, 'stock_quantity': 20, 'is_featured': False, 'is_available': True},
    {'name': 'Premium Watch Holder', 'slug': 'premium-watch-holder', 'category': 'Tech Gadgets', 'material': 'PLA', 'price': 299, 'description': 'Elegant watch display holder. Showcase your timepiece collection.', 'color': 'Black/White/Wood Finish', 'dimensions': '12cm x 10cm x 15cm', 'weight': 0.10, 'stock_quantity': 25, 'is_featured': False, 'is_available': True},
    {'name': 'Headphone Stand', 'slug': 'headphone-stand-new', 'category': 'Tech Gadgets', 'material': 'PLA', 'price': 399, 'description': 'Stylish headphone stand for desk organization. Stable base with curved hanger.', 'color': 'Black/White/Red', 'dimensions': '15cm x 12cm x 25cm', 'weight': 0.12, 'stock_quantity': 22, 'is_featured': False, 'is_available': True},
    
    # SPECIAL COLLECTIONS
    {'name': 'Perpetual Flip Calendar', 'slug': 'perpetual-flip-calendar', 'category': 'Special Collections', 'material': 'PLA', 'price': 699, 'description': 'Perpetual desk calendar with flip mechanism. Never-ending date display.', 'color': 'Wood/Black/White', 'dimensions': '16cm x 11cm x 9cm', 'weight': 0.18, 'stock_quantity': 15, 'is_featured': False, 'is_available': True},
    {'name': 'Stress Reliever Cube', 'slug': 'stress-cube', 'category': 'Special Collections', 'material': 'PLA', 'price': 299, 'description': 'Fidget cube with multiple interactive elements. Perfect desk toy for stress relief.', 'color': 'Multi-color/Custom', 'dimensions': '4cm x 4cm x 4cm', 'weight': 0.04, 'stock_quantity': 40, 'is_featured': False, 'is_available': True},
    {'name': 'Custom Cable Tag', 'slug': 'custom-cable-tag', 'category': 'Special Collections', 'material': 'PLA', 'price': 99, 'description': 'Personalized cable identification tags. Organize your cables efficiently.', 'color': 'All Colors Available', 'dimensions': '5cm x 2cm x 0.3cm', 'weight': 0.008, 'stock_quantity': 100, 'is_featured': False, 'is_available': True},
    {'name': 'Printed Name Plate', 'slug': 'printed-nameplate', 'category': 'Special Collections', 'material': 'PLA', 'price': 399, 'description': 'Custom 3D printed name plate for desk or door. Professional finish.', 'color': 'All Colors Available', 'dimensions': '20cm x 8cm x 1cm', 'weight': 0.06, 'stock_quantity': 30, 'is_featured': False, 'is_available': True},
    
    # SCULPTURES/CRAFTS
    {'name': 'Puppy Sculpture', 'slug': 'puppy-sculpture', 'category': 'Sculptures/Crafts', 'material': 'PLA', 'price': 299, 'description': 'Adorable puppy figurine with geometric design. Perfect decorative piece.', 'color': 'White/Gold/Custom', 'dimensions': '10cm x 8cm x 12cm', 'weight': 0.08, 'stock_quantity': 25, 'is_featured': False, 'is_available': True},
    {'name': 'Ganesh Idol', 'slug': 'ganesh-idol-new', 'category': 'Sculptures/Crafts', 'material': 'PLA', 'price': 299, 'description': 'Traditional Ganesh idol with intricate details. Spiritual decor piece.', 'color': 'Gold/White/Multi-color', 'dimensions': '12cm x 10cm x 8cm', 'weight': 0.10, 'stock_quantity': 30, 'is_featured': False, 'is_available': True},
    {'name': 'Lion Sculpture', 'slug': 'lion-sculpture', 'category': 'Sculptures/Crafts', 'material': 'PLA', 'price': 299, 'description': 'Majestic lion sculpture with geometric facets. Eye-catching decorative art.', 'color': 'Gold/Black/White', 'dimensions': '15cm x 10cm x 12cm', 'weight': 0.12, 'stock_quantity': 20, 'is_featured': False, 'is_available': True},
]

def add_products():
    """Add all new products to database"""
    
    # Create new categories
    new_categories = {
        'Lamps': 'Decorative lamps and lighting solutions',
        'Special Collections': 'Unique and special items',
        'Sculptures/Crafts': 'Artistic sculptures and craft pieces',
    }
    
    # Get or create all categories
    all_categories = {
        **new_categories,
        'Tech Gadgets': 'Smartphone accessories, laptop stands, and tech organizers',
        'Keychains': 'Custom and themed keychains',
    }
    
    for cat_name, cat_desc in all_categories.items():
        Category.objects.get_or_create(name=cat_name, defaults={'description': cat_desc})
        print(f"✓ Category: {cat_name}")
    
    # Ensure PLA material exists
    Material.objects.get_or_create(name='PLA', defaults={'description': 'Eco-friendly biodegradable plastic'})
    print(f"✓ Material: PLA")
    
    print("\n" + "="*50 + "\nAdding Products...\n" + "="*50 + "\n")
    
    added_count = updated_count = 0
    
    for product_data in products_data:
        category = Category.objects.get(name=product_data['category'])
        material = Material.objects.get(name=product_data['material'])
        
        product_info = product_data.copy()
        product_info.pop('category')
        product_info.pop('material')
        
        product, created = Product.objects.update_or_create(
            slug=product_info['slug'],
            defaults={**product_info, 'category': category, 'material': material, 'price': Decimal(str(product_info['price']))}
        )
        
        status = "✓ ADDED" if created else "↻ UPDATED"
        featured = " [FEATURED]" if product.is_featured else ""
        print(f"{status}: {product.name} - ₹{product.price}{featured}")
        
        if created:
            added_count += 1
        else:
            updated_count += 1
    
    # Show featured products summary
    featured_products = Product.objects.filter(is_featured=True)
    featured_by_category = {}
    for product in featured_products:
        cat = product.category.name
        if cat not in featured_by_category:
            featured_by_category[cat] = []
        featured_by_category[cat].append(product.name)
    
    print("\n" + "="*50)
    print(f"Summary:")
    print(f"  New products added: {added_count}")
    print(f"  Products updated: {updated_count}")
    print(f"  Total products: {Product.objects.count()}")
    print(f"  Featured products: {featured_products.count()}")
    print("\nFeatured Products by Category:")
    for cat, prods in featured_by_category.items():
        print(f"  {cat}: {len(prods)} products")
    print("="*50)
    print("\n✅ All products added successfully!")
    print("\nNext Steps:")
    print("1. Add product images to: PrintBox-Frontend/public/assets/products/")
    print("2. Update productImageMap.js with image filenames")
    print("3. Test products on frontend shop page")

if __name__ == '__main__':
    add_products()
