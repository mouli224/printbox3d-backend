"""
Quick environment variable checker for Railway deployment
Run this in Railway shell to diagnose configuration issues
"""

import os
import sys

print("\n" + "="*60)
print("RAILWAY ENVIRONMENT CONFIGURATION CHECK")
print("="*60 + "\n")

# Check Django Settings
print("1. DJANGO CONFIGURATION:")
print("-" * 40)
secret_key = os.getenv('SECRET_KEY', 'NOT SET')
print(f"   SECRET_KEY: {'✓ SET' if secret_key != 'NOT SET' else '✗ NOT SET'}")

debug = os.getenv('DEBUG', 'NOT SET')
print(f"   DEBUG: {debug}")

allowed_hosts = os.getenv('ALLOWED_HOSTS', 'NOT SET')
print(f"   ALLOWED_HOSTS: {allowed_hosts}")

# Check Database
print("\n2. DATABASE CONFIGURATION:")
print("-" * 40)
db_url = os.getenv('DATABASE_URL', 'NOT SET')
print(f"   DATABASE_URL: {'✓ SET' if db_url != 'NOT SET' else '✗ NOT SET'}")
if db_url != 'NOT SET':
    # Hide password in output
    if '@' in db_url:
        parts = db_url.split('@')
        safe_url = f"{parts[0].split(':')[0]}:***@{parts[1]}"
        print(f"   URL Preview: {safe_url}")

# Check Razorpay
print("\n3. RAZORPAY CONFIGURATION:")
print("-" * 40)
rzp_key_id = os.getenv('RAZORPAY_KEY_ID', 'NOT SET')
rzp_key_secret = os.getenv('RAZORPAY_KEY_SECRET', 'NOT SET')

print(f"   RAZORPAY_KEY_ID: {'✓ SET' if rzp_key_id != 'NOT SET' else '✗ NOT SET'}")
if rzp_key_id != 'NOT SET':
    print(f"   Key ID: {rzp_key_id}")

print(f"   RAZORPAY_KEY_SECRET: {'✓ SET' if rzp_key_secret != 'NOT SET' else '✗ NOT SET'}")
if rzp_key_secret != 'NOT SET':
    print(f"   Secret: {rzp_key_secret[:8]}...{rzp_key_secret[-4:]}")

# Check Email
print("\n4. EMAIL CONFIGURATION:")
print("-" * 40)
email_host = os.getenv('EMAIL_HOST', 'NOT SET')
email_user = os.getenv('EMAIL_HOST_USER', 'NOT SET')
email_pass = os.getenv('EMAIL_HOST_PASSWORD', 'NOT SET')

print(f"   EMAIL_HOST: {email_host}")
print(f"   EMAIL_HOST_USER: {'✓ SET' if email_user != 'NOT SET' else '✗ NOT SET'}")
print(f"   EMAIL_HOST_PASSWORD: {'✓ SET' if email_pass != 'NOT SET' else '✗ NOT SET'}")

# Check CORS/CSRF
print("\n5. SECURITY CONFIGURATION:")
print("-" * 40)
cors_origins = os.getenv('CORS_ALLOWED_ORIGINS', 'NOT SET')
csrf_origins = os.getenv('CSRF_TRUSTED_ORIGINS', 'NOT SET')

print(f"   CORS_ALLOWED_ORIGINS: {cors_origins if cors_origins != 'NOT SET' else '✗ NOT SET'}")
print(f"   CSRF_TRUSTED_ORIGINS: {csrf_origins if csrf_origins != 'NOT SET' else '✗ NOT SET'}")

# Summary
print("\n" + "="*60)
print("SUMMARY:")
print("="*60)

issues = []
if secret_key == 'NOT SET' or 'django-insecure' in secret_key:
    issues.append("⚠️  SECRET_KEY not set or using default insecure key")

if rzp_key_id == 'NOT SET':
    issues.append("⚠️  RAZORPAY_KEY_ID not set")

if rzp_key_secret == 'NOT SET':
    issues.append("⚠️  RAZORPAY_KEY_SECRET not set")

if db_url == 'NOT SET':
    issues.append("⚠️  DATABASE_URL not set")

if debug == 'True':
    issues.append("⚠️  DEBUG is True (should be False in production)")

if issues:
    print("\n❌ ISSUES FOUND:")
    for issue in issues:
        print(f"   {issue}")
    print("\n💡 FIX: Add missing environment variables in Railway Dashboard")
    sys.exit(1)
else:
    print("\n✅ All critical environment variables are configured!")
    print("\n🚀 Ready for deployment!")
    sys.exit(0)
