# PrintBox3D Backend - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd PrintBox-Backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Environment

Create a `.env` file in the root directory:

```env
SECRET_KEY=django-insecure-dev-key-for-local-development
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

### Step 3: Setup Database

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser
# Follow the prompts to set username, email, and password

# Load sample data (optional)
python manage.py populate_sample_data
```

### Step 4: Run Development Server

```bash
python manage.py runserver
```

🎉 Your API is now running at `http://localhost:8000/api/`

### Step 5: Access Admin Panel

Visit `http://localhost:8000/admin/` and login with your superuser credentials.

## 📡 Test API Endpoints

### Get Products
```bash
curl http://localhost:8000/api/products/
```

### Get Categories
```bash
curl http://localhost:8000/api/categories/
```

### Get Featured Products
```bash
curl http://localhost:8000/api/products/featured/
```

### Submit Custom Order (with curl)
```bash
curl -X POST http://localhost:8000/api/custom-orders/ \
  -F "name=John Doe" \
  -F "email=john@example.com" \
  -F "phone=+91 1234567890" \
  -F "material=PLA" \
  -F "color=Blue" \
  -F "description=Custom trophy design" \
  -F "quantity=1"
```

## 🔧 Common Commands

### Create new app
```bash
python manage.py startapp app_name
```

### Make migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Create superuser
```bash
python manage.py createsuperuser
```

### Load sample data
```bash
python manage.py populate_sample_data
```

### Collect static files
```bash
python manage.py collectstatic
```

### Run tests
```bash
python manage.py test
```

### Open Django shell
```bash
python manage.py shell
```

## 📱 Connect Your Frontend

In your React frontend, update the API URL:

```javascript
// src/config.js
export const API_URL = 'http://localhost:8000/api';

// Example: Fetch products
fetch(`${API_URL}/products/`)
  .then(res => res.json())
  .then(data => console.log(data));
```

## 🐛 Troubleshooting

### Port already in use?
```bash
# Run on different port
python manage.py runserver 8080
```

### Database locked?
```bash
# Delete and recreate database
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Module not found?
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### CORS errors?
Make sure your frontend URL is in `.env`:
```env
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
```

## 📚 Next Steps

1. **Customize Models**: Edit `api/models.py` to add fields
2. **Add Endpoints**: Create new views in `api/views.py`
3. **Admin Panel**: Customize `api/admin.py`
4. **Deploy**: Follow `DEPLOYMENT.md` for Railway deployment

## 📖 Documentation

- **API Documentation**: See `API_DOCUMENTATION.md`
- **Deployment Guide**: See `DEPLOYMENT.md`
- **Full README**: See `README.md`

## 🆘 Need Help?

- Check Django docs: https://docs.djangoproject.com
- Django REST Framework: https://www.django-rest-framework.org
- Create an issue on GitHub

---

**Happy Coding! 🎉**
