import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'printbox_backend.settings')
django.setup()

from api.models import Product

# Image mappings based on product slugs
image_mappings = {
    # Lamps
    'ocean-drift-lamp': 'products/lamps/ocean-drift-lamp/ocean-drift-lamp1.webp',
    'tide-form-lamp': 'products/lamps/tide-form-lamp/tide-form-lamp1.webp',
    'reindeer-lamp-set': 'products/lamps/reindeer-lamp-set/reindeer-lamp-set1.webp',
    'christmas-tree-lamp': 'products/lamps/christmas-tree-lamp/christmas-tree-lamp1.webp',
    'round-christmas-lamp': 'products/lamps/round-christmas-lamp/round-christmas-lamp1.webp',
    
    # Keychains
    'spotify-keychain': 'products/keychains/spotify-keychain/spotify-keychain1.webp',
    'number-plate-keychain': 'products/keychains/number-plate-keychain/number-plate-keychain1.webp',
    'octopus-keychain-new': 'products/keychains/octopus-keychain/octopus-keychain1.webp',
    'gym-weight-keychain': 'products/keychains/gym-weight-keychain/gym-weight-keychain1.webp',
    'dumbbell-keychain': 'products/keychains/dumbbell-keychain/dumbbell-keychain1.webp',
    'mobile-stand-keychain': 'products/keychains/mobile-stand-keychain/mobile-stand-keychain1.webp',
    'engine-keychain': 'products/keychains/engine-keychain/engine-keychain1.webp',
    'xox-game-keychain': 'products/keychains/xox-game-keychain/xox-game-keychain1.webp',
    'zipper-tag-keychain': 'products/keychains/zipper-tag-keychain/zipper-tag-keychain1.webp',
    
    # Tech Gadgets
    'gear-mobile-holder': 'products/tech-gadgets/gear-mobile-holder/gear-mobile-holder1.webp',
    'premium-watch-holder': 'products/tech-gadgets/premium-watch-holder/premium-watch-holder1.webp',
    'headphone-stand-new': 'products/tech-gadgets/headphone-stand/headphone-stand1.webp',
    'perpetual-flip-calendar': 'products/tech-gadgets/perpetual-flip-calendar/perpetual-flip-calendar1.webp',
    'stress-cube': 'products/tech-gadgets/stress-cube/stress-cube1.webp',
    'custom-cable-tag': 'products/tech-gadgets/custom-cable-tag/custom-cable-tag1.webp',
    'printed-nameplate': 'products/tech-gadgets/printed-nameplate/printed-nameplate1.webp',
    
    # Sculptures
    'puppy-sculpture': 'products/sculptures/puppy-sculpture/puppy-sculpture1.webp',
    'ganesh-idol-new': 'products/sculptures/ganesh-idol/ganesh-idol1.webp',
    'lion-sculpture': 'products/sculptures/lion-sculpture/lion-sculpture1.webp',
}

print("Fixing product images...")
updated_count = 0

for slug, image_path in image_mappings.items():
    try:
        product = Product.objects.get(slug=slug)
        if not product.image or product.image == '':
            product.image = image_path
            product.save()
            print(f"✓ Updated {product.name}: {image_path}")
            updated_count += 1
        else:
            print(f"- Skipped {product.name} (already has image: {product.image})")
    except Product.DoesNotExist:
        print(f"✗ Product not found: {slug}")

print(f"\nCompleted! Updated {updated_count} products.")
