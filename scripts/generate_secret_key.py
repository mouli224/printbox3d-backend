from django.core.management.utils import get_random_secret_key

print("\n=== PRODUCTION SECRET_KEY ===")
print(get_random_secret_key())
print("\nAdd this to your Railway environment variables as SECRET_KEY")
print("=" * 50)
