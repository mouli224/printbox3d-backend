"""
Script to add all products from PrintBox3D catalog
Run: python add_all_products.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'printbox_backend.settings')
django.setup()

from api.models import Product, Category, Material
from decimal import Decimal

# Product data from catalog (weight in kg)
products_data = [
    # Tech Gadgets
    {'name': '3D Printed Phone Stand', 'slug': 'phone-stand', 'category': 'Tech Gadgets', 'material': 'PLA', 'price': 299, 'description': 'Stylish and functional phone stand for your desk. Adjustable angle for comfortable viewing.', 'color': 'Black/White/Custom', 'dimensions': '12cm x 8cm x 10cm', 'weight': 0.05, 'stock_quantity': 25, 'is_featured': True, 'is_available': True},
    {'name': 'Laptop Stand', 'slug': 'laptop-stand', 'category': 'Tech Gadgets', 'material': 'PLA', 'price': 799, 'description': 'Ergonomic laptop stand for better posture and improved airflow. Adjustable height and angle.', 'color': 'Black/White/Gray', 'dimensions': '28cm x 20cm x 15cm', 'weight': 0.25, 'stock_quantity': 15, 'is_featured': True, 'is_available': True},
    {'name': 'Headphone Stand', 'slug': 'headphone-stand', 'category': 'Tech Gadgets', 'material': 'PLA', 'price': 399, 'description': 'Elegant headphone stand to organize your desk. Stable base with curved design.', 'color': 'Black/White/Wood Finish', 'dimensions': '15cm x 12cm x 25cm', 'weight': 0.12, 'stock_quantity': 20, 'is_featured': False, 'is_available': True},
    {'name': 'Cable Organizer', 'slug': 'cable-organizer', 'category': 'Tech Gadgets', 'material': 'PLA', 'price': 199, 'description': 'Cable management solution for desk and office. Multiple slots for different cable sizes.', 'color': 'Black/White', 'dimensions': '10cm x 5cm x 3cm', 'weight': 0.03, 'stock_quantity': 50, 'is_featured': False, 'is_available': True},
    {'name': 'Watch Stand', 'slug': 'watch-stand', 'category': 'Tech Gadgets', 'material': 'PLA', 'price': 349, 'description': 'Premium watch display stand. Perfect for showcasing your watch collection.', 'color': 'Black/Gold/Silver', 'dimensions': '10cm x 8cm x 12cm', 'weight': 0.08, 'stock_quantity': 15, 'is_featured': False, 'is_available': True},
    
    # Home Decor
    {'name': 'Wall Shelf', 'slug': 'wall-shelf', 'category': 'Home Decor', 'material': 'PLA', 'price': 599, 'description': 'Decorative wall shelf for books, plants, or decorative items. Easy to mount.', 'color': 'White/Wood/Black', 'dimensions': '30cm x 15cm x 8cm', 'weight': 0.20, 'stock_quantity': 10, 'is_featured': False, 'is_available': True},
    {'name': 'Decorative Vase', 'slug': 'decorative-vase', 'category': 'Home Decor', 'material': 'PLA', 'price': 449, 'description': 'Modern geometric vase design. Perfect for artificial or dried flowers.', 'color': 'White/Black/Gold', 'dimensions': '15cm x 15cm x 20cm', 'weight': 0.15, 'stock_quantity': 12, 'is_featured': True, 'is_available': True},
    {'name': '3D Printed Clock', 'slug': '3d-clock', 'category': 'Home Decor', 'material': 'PLA', 'price': 899, 'description': 'Unique wall clock with customizable design. Battery-operated movement included.', 'color': 'Custom Colors', 'dimensions': '25cm diameter', 'weight': 0.18, 'stock_quantity': 8, 'is_featured': True, 'is_available': True},
    {'name': 'Ganesh Idol', 'slug': 'ganesh-idol', 'category': 'Home Decor', 'material': 'PLA', 'price': 699, 'description': 'Traditional Ganesh idol with intricate details. Perfect for pooja room or home decor.', 'color': 'Gold/White/Multi-color', 'dimensions': '15cm x 12cm x 8cm', 'weight': 0.12, 'stock_quantity': 20, 'is_featured': False, 'is_available': True},
    {'name': 'Christmas Lamp', 'slug': 'christmas-lamp', 'category': 'Home Decor', 'material': 'PLA', 'price': 799, 'description': 'Festive Christmas-themed decorative lamp. LED lights create warm ambiance.', 'color': 'White/Red/Green', 'dimensions': '20cm x 15cm x 15cm', 'weight': 0.20, 'stock_quantity': 15, 'is_featured': True, 'is_available': True},
    {'name': 'Christmas Tree Decoration', 'slug': 'christmas-tree', 'category': 'Home Decor', 'material': 'PLA', 'price': 499, 'description': 'Miniature Christmas tree decoration. Perfect for desk or tabletop display.', 'color': 'Green/White/Multi-color', 'dimensions': '18cm x 12cm x 12cm', 'weight': 0.10, 'stock_quantity': 25, 'is_featured': False, 'is_available': True},
    
    # Keychains & Accessories
    {'name': 'Custom Name Keychain', 'slug': 'custom-keychain', 'category': 'Keychains', 'material': 'PLA', 'price': 149, 'description': 'Personalized keychain with custom name or text. Perfect gift item.', 'color': 'All Colors Available', 'dimensions': '8cm x 3cm x 0.5cm', 'weight': 0.015, 'stock_quantity': 100, 'is_featured': True, 'is_available': True},
    {'name': 'Morse Code Keychain', 'slug': 'morse-keychain', 'category': 'Keychains', 'material': 'PLA', 'price': 179, 'description': 'Unique keychain with your name in Morse code. Great conversation starter.', 'color': 'Black/White/Custom', 'dimensions': '10cm x 2cm x 0.5cm', 'weight': 0.012, 'stock_quantity': 50, 'is_featured': True, 'is_available': True},
    {'name': 'Octopus Keychain', 'slug': 'octopus-keychain', 'category': 'Keychains', 'material': 'TPU', 'price': 199, 'description': 'Flexible octopus keychain with moving tentacles. Fun and durable.', 'color': 'Blue/Pink/Green', 'dimensions': '6cm x 6cm x 4cm', 'weight': 0.02, 'stock_quantity': 40, 'is_featured': False, 'is_available': True},
    
    # Office Supplies
    {'name': 'Pen Holder', 'slug': 'pen-holder', 'category': 'Office Supplies', 'material': 'PLA', 'price': 299, 'description': 'Multi-compartment pen and pencil holder. Organize your desk essentials.', 'color': 'Black/White/Gray', 'dimensions': '12cm x 8cm x 10cm', 'weight': 0.10, 'stock_quantity': 30, 'is_featured': False, 'is_available': True},
    {'name': 'Flip Calendar', 'slug': 'flip-calendar', 'category': 'Office Supplies', 'material': 'PLA', 'price': 599, 'description': 'Perpetual desk calendar. Manually adjustable date display.', 'color': 'Wood/Black/White', 'dimensions': '15cm x 10cm x 8cm', 'weight': 0.15, 'stock_quantity': 15, 'is_featured': False, 'is_available': True},
    
    # Fitness & Wellness
    {'name': 'Decorative Dumbbell', 'slug': 'decorative-dumbbell', 'category': 'Fitness', 'material': 'PLA', 'price': 399, 'description': 'Miniature decorative dumbbell. Perfect for fitness enthusiasts desk decor.', 'color': 'Black/Silver/Custom', 'dimensions': '15cm x 6cm x 6cm', 'weight': 0.08, 'stock_quantity': 20, 'is_featured': False, 'is_available': True},
]

def add_products():
    """Add all products to database"""
    
    # Create categories
    categories = {
        'Tech Gadgets': 'Smartphone accessories, laptop stands, and tech organizers',
        'Home Decor': 'Wall art, decorative items, and home accessories',
        'Keychains': 'Custom and themed keychains',
        'Office Supplies': 'Desk organizers and office accessories',
        'Fitness': 'Fitness-themed decorative items',
    }
    
    for cat_name, cat_desc in categories.items():
        Category.objects.get_or_create(name=cat_name, defaults={'description': cat_desc})
        print(f"✓ Category: {cat_name}")
    
    # Create materials
    materials = {'PLA': 'Eco-friendly biodegradable plastic', 'TPU': 'Flexible rubber-like material'}
    
    for mat_name, mat_desc in materials.items():
        Material.objects.get_or_create(name=mat_name, defaults={'description': mat_desc})
        print(f"✓ Material: {mat_name}")
    
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
        
        if created:
            added_count += 1
            print(f"✓ ADDED: {product.name} - ₹{product.price}")
        else:
            updated_count += 1
            print(f"↻ UPDATED: {product.name} - ₹{product.price}")
    
    print("\n" + "="*50)
    print(f"Summary:\n  New products added: {added_count}\n  Products updated: {updated_count}\n  Total products: {Product.objects.count()}")
    print("="*50)
    print("\n✅ All products added successfully!\n\nNext Steps:\n1. Add product images to: PrintBox-Frontend/public/assets/products/\n2. Update productImageMap.js with image filenames\n3. Test products on frontend: http://localhost:3000/shop")

if __name__ == '__main__':
    add_products()
