import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'printbox_backend.settings')
django.setup()

from api.models import Product, Category, Material

# Get or create category and material
category, _ = Category.objects.get_or_create(
    slug='tech-gadgets',
    defaults={'name': 'Tech Gadgets', 'description': 'Tech accessories and gadgets'}
)

material, _ = Material.objects.get_or_create(
    name='PLA',
    defaults={'description': 'Standard PLA plastic'}
)

# Create test product
test_product = Product.objects.create(
    name='Test Product - ₹1',
    slug='test-product-1-rupee',
    description='Test product for payment testing - Only ₹1',
    price=1.00,
    original_price=1.11,  # 10% discount
    discount_percentage=10.00,
    category=category,
    material=material,
    weight=0.01,
    dimensions='1x1x1 cm',
    stock_quantity=999,
    is_available=True,
    is_featured=False,
    frontend_image='test-product.jpg',
    image='products/test.jpg'  # Placeholder
)

print(f"\n✅ Test product created successfully!")
print(f"   ID: {test_product.id}")
print(f"   Name: {test_product.name}")
print(f"   Price: ₹{test_product.price}")
print(f"   Category: {test_product.category.name}")
print(f"\n🧪 Use this product for testing payments with minimal cost!")
