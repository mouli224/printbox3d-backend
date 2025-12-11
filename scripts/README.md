# Backend Utility Scripts

This directory contains utility scripts for managing products, testing, and deployment diagnostics.

## Product Management Scripts

### `add_products.py`
**Purpose**: Populate database with initial product catalog  
**Usage**: `python scripts/add_products.py`  
**When to use**: First-time database setup or adding new products

### `add_test_product.py`
**Purpose**: Create a ₹1 test product for payment testing  
**Usage**: `python scripts/add_test_product.py`  
**When to use**: Testing payment flow without spending real money

### `split_keychains.py`
**Purpose**: Split keychain product into separate variants  
**Usage**: `python scripts/split_keychains.py`  
**When to use**: Product catalog restructuring

### `add_discount.py`
**Purpose**: Add discount percentages to existing products  
**Usage**: `python scripts/add_discount.py`  
**When to use**: Running promotions or updating pricing

### `add_new_products.py`
**Purpose**: Add specific new products to catalog  
**Usage**: `python scripts/add_new_products.py`  
**When to use**: Expanding product inventory

### `add_all_products.py`
**Purpose**: Comprehensive product catalog initialization  
**Usage**: `python scripts/add_all_products.py`  
**When to use**: Complete database reset with full catalog

## Deployment & Diagnostics

### `check_env.py`
**Purpose**: Verify Railway environment variables  
**Usage**: Run in Railway shell: `python scripts/check_env.py`  
**When to use**: Debugging deployment configuration issues

### `generate_secret_key.py`
**Purpose**: Generate secure Django SECRET_KEY  
**Usage**: `python scripts/generate_secret_key.py`  
**When to use**: Production deployment setup

## Important Notes

⚠️ **Before running any script:**
1. Ensure Django environment is configured (`manage.py` accessible)
2. Database connection is working
3. You understand what the script does (check source code)

⚠️ **Product scripts modify the database directly** - backup before running in production!
