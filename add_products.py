import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'printbox_backend.settings')
django.setup()

from api.models import Product, Category, Material

# Get or create categories
home_decor, _ = Category.objects.get_or_create(
    slug='home-decor',
    defaults={
        'name': 'Home Decor',
        'description': 'Beautiful decorative items for your home'
    }
)

accessories, _ = Category.objects.get_or_create(
    slug='accessories',
    defaults={
        'name': 'Accessories',
        'description': 'Functional and stylish accessories'
    }
)

gadgets, _ = Category.objects.get_or_create(
    slug='gadgets',
    defaults={
        'name': 'Gadgets',
        'description': 'Tech accessories and organizers'
    }
)

seasonal, _ = Category.objects.get_or_create(
    slug='seasonal',
    defaults={
        'name': 'Seasonal',
        'description': 'Seasonal and festive decorations'
    }
)

fitness, _ = Category.objects.get_or_create(
    slug='fitness',
    defaults={
        'name': 'Fitness',
        'description': 'Fitness and wellness accessories'
    }
)

# Get or create materials
pla, _ = Material.objects.get_or_create(
    name='PLA',
    defaults={
        'description': 'Biodegradable thermoplastic, eco-friendly',
        'properties': 'Lightweight, biodegradable, smooth finish'
    }
)

abs_material, _ = Material.objects.get_or_create(
    name='ABS',
    defaults={
        'description': 'Strong and durable thermoplastic',
        'properties': 'Impact resistant, durable, heat resistant'
    }
)

petg, _ = Material.objects.get_or_create(
    name='PETG',
    defaults={
        'description': 'Strong and flexible material',
        'properties': 'Impact resistant, flexible, chemical resistant'
    }
)

# Products data
products_data = [
    {
        'slug': 'christmas-lamp',
        'name': 'Christmas Lamp',
        'description': 'Beautiful 3D printed Christmas lamp with intricate lattice design. Perfect for adding festive ambiance to your home during the holiday season. Features LED-compatible design for warm, cozy lighting.',
        'category': seasonal,
        'material': pla,
        'price': 899.00,
        'color': 'White/Red',
        'dimensions': '15cm x 15cm x 20cm',
        'weight': 180,
        'stock_quantity': 10,
        'is_featured': True
    },
    {
        'slug': 'christmas-tree',
        'name': 'Christmas Tree',
        'description': 'Elegant spiral Christmas tree decoration, perfect for tabletop display. Modern minimalist design that adds festive charm to any space. Lightweight and easy to display.',
        'category': seasonal,
        'material': pla,
        'price': 599.00,
        'color': 'Red/Green',
        'dimensions': '12cm x 12cm x 25cm',
        'weight': 120,
        'stock_quantity': 10,
        'is_featured': True
    },
    {
        'slug': 'dumbell',
        'name': 'Decorative Dumbell',
        'description': 'Stylish decorative dumbell weight perfect for fitness enthusiasts or gym decor. Lightweight 3D printed design, ideal for motivational display or as a paperweight.',
        'category': fitness,
        'material': abs_material,
        'price': 349.00,
        'color': 'Black/Blue',
        'dimensions': '15cm x 8cm x 8cm',
        'weight': 200,
        'stock_quantity': 10
    },
    {
        'slug': 'flip-calendar',
        'name': 'Flip Calendar',
        'description': 'Vintage-style flip calendar with retro orange and black design. Functional desk accessory that adds character to your workspace. Manual flip mechanism for date display.',
        'category': gadgets,
        'material': abs_material,
        'price': 799.00,
        'color': 'Orange/Black',
        'dimensions': '12cm x 10cm x 8cm',
        'weight': 150,
        'stock_quantity': 10
    },
    {
        'slug': 'keychain',
        'name': 'Designer Keychain',
        'description': 'Unique 3D printed keychain set including morse code and octopus designs. Durable and lightweight, perfect for personalizing your keys or bags. Makes a great gift item.',
        'category': accessories,
        'material': pla,
        'price': 199.00,
        'color': 'Multi-color',
        'dimensions': '5cm x 3cm x 1cm',
        'weight': 15,
        'stock_quantity': 10,
        'is_featured': True
    },
    {
        'slug': 'phone-stand',
        'name': 'Phone Stand',
        'description': 'Ergonomic phone stand with optimal viewing angle. Perfect for video calls, watching content, or hands-free use. Non-slip base keeps your device secure.',
        'category': gadgets,
        'material': pla,
        'price': 299.00,
        'color': 'White/Black',
        'dimensions': '10cm x 8cm x 12cm',
        'weight': 80,
        'stock_quantity': 10,
        'is_featured': True
    },
    {
        'slug': 'laptop-stand',
        'name': 'Laptop Stand',
        'description': 'Adjustable laptop stand for improved ergonomics and posture. Elevates your laptop to eye level, reducing neck strain. Sturdy design with ventilation for better cooling.',
        'category': gadgets,
        'material': abs_material,
        'price': 1299.00,
        'color': 'Silver/Gray',
        'dimensions': '25cm x 20cm x 15cm',
        'weight': 400,
        'stock_quantity': 10
    },
    {
        'slug': 'watch-stand',
        'name': 'Watch Stand',
        'description': 'Elegant watch display stand perfect for organizing and showcasing your timepiece collection. Soft-touch surface protects your watches from scratches.',
        'category': accessories,
        'material': pla,
        'price': 399.00,
        'color': 'Wood/Beige',
        'dimensions': '8cm x 8cm x 10cm',
        'weight': 60,
        'stock_quantity': 10
    },
    {
        'slug': 'cable-organizer',
        'name': 'Cable Organizer',
        'description': 'Practical cable management solution to keep your desk tidy. Multiple slots for organizing various cable sizes. Adhesive base for easy mounting.',
        'category': gadgets,
        'material': pla,
        'price': 249.00,
        'color': 'Gray/Black',
        'dimensions': '8cm x 5cm x 3cm',
        'weight': 40,
        'stock_quantity': 10
    },
    {
        'slug': 'decorative-vase',
        'name': 'Decorative Vase',
        'description': 'Modern geometric vase with unique spiral design. Perfect for dried flowers or as a standalone decorative piece. Adds contemporary elegance to any room.',
        'category': home_decor,
        'material': pla,
        'price': 699.00,
        'color': 'White/Cream',
        'dimensions': '12cm x 12cm x 25cm',
        'weight': 200,
        'stock_quantity': 10,
        'is_featured': True
    },
    {
        'slug': 'headphone-stand',
        'name': 'Headphone Stand',
        'description': 'Premium headphone stand to keep your audio gear organized and on display. Curved design prevents headband deformation. Weighted base for stability.',
        'category': gadgets,
        'material': abs_material,
        'price': 549.00,
        'color': 'Black',
        'dimensions': '15cm x 12cm x 25cm',
        'weight': 250,
        'stock_quantity': 10
    },
    {
        'slug': 'wall-shelf',
        'name': 'Wall Shelf',
        'description': 'Minimalist wall-mounted shelf perfect for small plants, photos, or decorative items. Easy to install with included mounting hardware. Modern floating design.',
        'category': home_decor,
        'material': petg,
        'price': 799.00,
        'color': 'White',
        'dimensions': '30cm x 15cm x 5cm',
        'weight': 300,
        'stock_quantity': 10
    },
    {
        'slug': 'clock',
        'name': 'Designer Wall Clock',
        'description': 'Contemporary wall clock with unique geometric design. Silent quartz movement ensures no ticking sound. Adds modern style to any room.',
        'category': home_decor,
        'material': pla,
        'price': 1099.00,
        'color': 'Black/White',
        'dimensions': '30cm x 30cm x 5cm',
        'weight': 350,
        'stock_quantity': 10
    },
    {
        'slug': 'ganesh-idol',
        'name': 'Ganesh Idol',
        'description': 'Beautifully detailed Lord Ganesh idol for spiritual decor. Perfect for home temple, office desk, or as a thoughtful gift. Intricate detailing showcases craftsmanship.',
        'category': home_decor,
        'material': pla,
        'price': 899.00,
        'color': 'Gold/Orange',
        'dimensions': '15cm x 10cm x 20cm',
        'weight': 180,
        'stock_quantity': 10,
        'is_featured': True
    }
]

# Create or update products
created_count = 0
updated_count = 0

for product_data in products_data:
    product, created = Product.objects.update_or_create(
        slug=product_data['slug'],
        defaults=product_data
    )
    
    if created:
        created_count += 1
        print(f"✓ Created: {product.name}")
    else:
        updated_count += 1
        print(f"↻ Updated: {product.name}")

print(f"\n{'='*50}")
print(f"Products created: {created_count}")
print(f"Products updated: {updated_count}")
print(f"Total products: {created_count + updated_count}")
print(f"{'='*50}")
