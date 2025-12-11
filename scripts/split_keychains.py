import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'printbox_backend.settings')
django.setup()

from api.models import Product, Category, Material

def split_keychains():
    """Split the keychain product into two separate products"""
    
    # Get the existing keychain product
    try:
        keychain = Product.objects.get(slug='keychain')
        print(f"Found existing keychain: {keychain.name}")
        
        # Get category and material
        accessories_category = Category.objects.get(name='Accessories')
        pla_material = Material.objects.get(name='PLA')
        
        # Create Morse Code Keychain
        morse_keychain, created = Product.objects.update_or_create(
            slug='morse-code-keychain',
            defaults={
                'name': 'Morse Code Keychain',
                'description': 'Personalized morse code keychain that translates your special message into dots and dashes. A unique accessory that carries hidden meaning wherever you go. Perfect gift for loved ones, friends, or anyone who appreciates coded messages.',
                'price': 199.00,
                'category': accessories_category,
                'material': pla_material,
                'color': 'Red & White',
                'dimensions': '5cm x 3cm x 1cm',
                'weight': 15.00,
                'stock_quantity': 10,
                'is_available': True,
                'is_featured': True,
                'frontend_image': 'morsecode-keychain'
            }
        )
        print(f"{'Created' if created else 'Updated'} Morse Code Keychain (ID: {morse_keychain.id})")
        
        # Create Octopus Keychain
        octopus_keychain, created = Product.objects.update_or_create(
            slug='octopus-keychain',
            defaults={
                'name': 'Octopus Keychain',
                'description': 'Adorable 3D printed octopus keychain with articulated tentacles. This cute marine creature makes a fun and unique accessory for your keys, bags, or backpacks. Lightweight, durable, and full of personality.',
                'price': 149.00,
                'category': accessories_category,
                'material': pla_material,
                'color': 'Blue & Multi-color',
                'dimensions': '4cm x 4cm x 2cm',
                'weight': 12.00,
                'stock_quantity': 10,
                'is_available': True,
                'is_featured': False,
                'frontend_image': 'octopus-keychain'
            }
        )
        print(f"{'Created' if created else 'Updated'} Octopus Keychain (ID: {octopus_keychain.id})")
        
        # Delete the old generic keychain
        keychain.delete()
        print(f"Deleted old generic keychain product")
        
        print("\n✅ Successfully split keychain into two separate products:")
        print(f"   1. Morse Code Keychain (₹199.00) - Featured")
        print(f"   2. Octopus Keychain (₹149.00)")
        
    except Product.DoesNotExist:
        print("❌ Keychain product not found. It may have already been split.")
        
        # Create products anyway
        accessories_category = Category.objects.get(name='Accessories')
        pla_material = Material.objects.get(name='PLA')
        
        morse_keychain, _ = Product.objects.get_or_create(
            slug='morse-code-keychain',
            defaults={
                'name': 'Morse Code Keychain',
                'description': 'Personalized morse code keychain that translates your special message into dots and dashes. A unique accessory that carries hidden meaning wherever you go. Perfect gift for loved ones, friends, or anyone who appreciates coded messages.',
                'price': 199.00,
                'category': accessories_category,
                'material': pla_material,
                'color': 'Red & White',
                'dimensions': '5cm x 3cm x 1cm',
                'weight': 15.00,
                'stock_quantity': 10,
                'is_available': True,
                'is_featured': True,
                'frontend_image': 'morsecode-keychain'
            }
        )
        
        octopus_keychain, _ = Product.objects.get_or_create(
            slug='octopus-keychain',
            defaults={
                'name': 'Octopus Keychain',
                'description': 'Adorable 3D printed octopus keychain with articulated tentacles. This cute marine creature makes a fun and unique accessory for your keys, bags, or backpacks. Lightweight, durable, and full of personality.',
                'price': 149.00,
                'category': accessories_category,
                'material': pla_material,
                'color': 'Blue & Multi-color',
                'dimensions': '4cm x 4cm x 2cm',
                'weight': 12.00,
                'stock_quantity': 10,
                'is_available': True,
                'is_featured': False,
                'frontend_image': 'octopus-keychain'
            }
        )
        
        print("✅ Created both keychain products")

if __name__ == '__main__':
    split_keychains()
