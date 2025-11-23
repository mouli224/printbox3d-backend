#!/usr/bin/env python
"""
Initial setup script for PrintBox3D Backend
Run this script after installing dependencies to set up the project
"""

import os
import sys
import subprocess
import secrets


def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"\n{'='*60}")
    print(f"🔧 {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        print(f"✅ {description} - Success!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed!")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False


def create_env_file():
    """Create .env file if it doesn't exist"""
    if os.path.exists('.env'):
        print("\n⚠️  .env file already exists. Skipping creation.")
        return

    print("\n🔐 Generating SECRET_KEY...")
    secret_key = secrets.token_urlsafe(50)
    
    env_content = f"""# Django Settings
SECRET_KEY={secret_key}
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (for local development - SQLite)
DATABASE_URL=

# CORS Settings (add your frontend URL)
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://printbox3d.com

# Email Settings (optional - for notifications)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ .env file created successfully!")


def main():
    """Main setup function"""
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║                                                            ║
    ║         PrintBox3D Backend - Initial Setup                 ║
    ║                                                            ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    # Check if virtual environment is activated
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Warning: Virtual environment is not activated!")
        print("   Consider activating it first:")
        print("   - Windows: venv\\Scripts\\activate")
        print("   - Mac/Linux: source venv/bin/activate\n")
        
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return
    
    # Create .env file
    create_env_file()
    
    # Run migrations
    if not run_command("python manage.py makemigrations", "Creating migrations"):
        return
    
    if not run_command("python manage.py migrate", "Applying migrations"):
        return
    
    # Ask if user wants to create sample data
    print("\n" + "="*60)
    response = input("📦 Do you want to populate the database with sample data? (Y/n): ")
    if response.lower() != 'n':
        run_command("python manage.py populate_sample_data", "Loading sample data")
    
    # Ask if user wants to create superuser
    print("\n" + "="*60)
    response = input("👤 Do you want to create a superuser account? (Y/n): ")
    if response.lower() != 'n':
        print("\n📝 Please enter superuser details:")
        os.system("python manage.py createsuperuser")
    
    # Collect static files
    run_command("python manage.py collectstatic --noinput", "Collecting static files")
    
    # Success message
    print("""
    
    ╔════════════════════════════════════════════════════════════╗
    ║                                                            ║
    ║              ✅ Setup Complete! 🎉                         ║
    ║                                                            ║
    ╚════════════════════════════════════════════════════════════╝
    
    🚀 Next Steps:
    
    1. Start the development server:
       python manage.py runserver
    
    2. Access the API:
       http://localhost:8000/api/
    
    3. Access the admin panel:
       http://localhost:8000/admin/
    
    4. Test the API endpoints:
       - Products: http://localhost:8000/api/products/
       - Categories: http://localhost:8000/api/categories/
       - Materials: http://localhost:8000/api/materials/
    
    📚 Documentation:
    - README.md - Full documentation
    - QUICKSTART.md - Quick start guide
    - API_DOCUMENTATION.md - API reference
    - DEPLOYMENT.md - Railway deployment guide
    
    🆘 Need Help?
    - Check the documentation files
    - Visit Django docs: https://docs.djangoproject.com
    - Create an issue on GitHub
    
    Happy coding! 🎨
    """)


if __name__ == "__main__":
    main()
