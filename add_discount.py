"""
Script to add 10% discount to all products
Run: python add_discount.py
"""

import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'printbox_backend.settings')
django.setup()

from api.models import Product

def add_discount_to_all_products():
    """Add 10% discount to all products"""
    
    print('\n🎯 Adding 10% discount to all products...\n')
    print('='*60)
    
    products = Product.objects.all()
    updated_count = 0
    
    for product in products:
        # Current price becomes the discounted price
        current_price = product.price
        
        # Calculate original price (10% higher)
        # If current price is X, and it's after 10% discount:
        # X = Original * 0.9
        # Original = X / 0.9 = X * (10/9)
        original_price = (current_price * Decimal('10')) / Decimal('9')
        original_price = original_price.quantize(Decimal('0.01'))
        
        # Update product
        product.original_price = original_price
        product.discount_percentage = Decimal('10.00')
        product.save()
        
        updated_count += 1
        print(f'✓ {product.name}')
        print(f'  Original: ₹{original_price} → Discounted: ₹{current_price} (10% OFF)')
        print()
    
    print('='*60)
    print(f'\n✅ Updated {updated_count} products with 10% discount!')
    print('\nDiscount Summary:')
    print(f'  Total products: {updated_count}')
    print(f'  Discount: 10% OFF')
    print(f'  Original prices calculated automatically')
    print('='*60 + '\n')

if __name__ == '__main__':
    add_discount_to_all_products()
