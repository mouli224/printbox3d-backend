# PrintBox3D Backend API

Django REST API backend for PrintBox3D - A 3D printing e-commerce website.

## 🚀 Features

- **Product Management**: CRUD operations for products, categories, and materials
- **Custom Orders**: Handle custom 3D printing requests with file uploads
- **Contact Forms**: Contact message and newsletter subscription handling
- **Testimonials**: Customer testimonials management
- **JWT Authentication**: Secure user registration and login with token-based auth
- **Admin Panel**: Full-featured Django admin for content management
- **REST API**: Complete RESTful API with DRF
- **Supabase PostgreSQL**: Production-ready database with connection pooling
- **Railway Ready**: Configured for easy deployment to Railway

## 📋 Requirements

- Python 3.11+
- PostgreSQL (Supabase for production)
- SQLite (for local development)
- Node.js (optional, for Railway CLI)

## 🛠️ Local Development Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd PrintBox-Backend
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://printbox3d.com
```

### 5. Database Setup

**Option A: Local Development (SQLite)**
```bash
# Leave DATABASE_URL empty in .env file
python manage.py migrate
python manage.py createsuperuser
```

**Option B: Supabase PostgreSQL**
```bash
# Update .env with your Supabase credentials
DATABASE_URL=postgresql://postgres.xxx:PASSWORD@xxx.supabase.com:6543/postgres?pgbouncer=true
DIRECT_DATABASE_URL=postgresql://postgres.xxx:PASSWORD@xxx.supabase.com:5432/postgres

# Run migrations
python manage.py migrate
python manage.py createsuperuser
```

See **[SUPABASE_RAILWAY_DEPLOYMENT.md](./SUPABASE_RAILWAY_DEPLOYMENT.md)** for detailed setup instructions.

### 6. Run development server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

Admin panel: `http://localhost:8000/admin/`

## 📡 API Endpoints

### Products

- `GET /api/products/` - List all products
- `GET /api/products/{slug}/` - Get product detail
- `GET /api/products/featured/` - Get featured products
- `GET /api/products/best_sellers/` - Get best sellers

**Query Parameters:**
- `category__slug` - Filter by category slug
- `material__name` - Filter by material name
- `is_featured` - Filter featured products
- `search` - Search in name and description
- `ordering` - Sort by: price, name, created_at

### Categories

- `GET /api/categories/` - List all categories
- `GET /api/categories/{slug}/` - Get category detail

### Materials

- `GET /api/materials/` - List all materials
- `GET /api/materials/{id}/` - Get material detail

### Custom Orders

- `POST /api/custom-orders/` - Submit a custom order request

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+91 1234567890",
  "material": "PLA",
  "color": "Blue",
  "description": "I need a custom trophy...",
  "quantity": 1,
  "budget": "1000-2000",
  "design_file": "<file upload>"
}
```

### Contact Messages

- `POST /api/contact/` - Submit a contact message

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "subject": "Product Inquiry",
  "message": "I would like to know more about..."
}
```

### Newsletter

- `POST /api/newsletter/` - Subscribe to newsletter

**Request Body:**
```json
{
  "email": "john@example.com"
}
```

### Testimonials

- `GET /api/testimonials/` - List all testimonials
- `GET /api/testimonials/featured/` - Get featured testimonials

### Authentication

- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login user (returns JWT tokens)
- `POST /api/auth/token/refresh/` - Refresh access token
- `GET /api/auth/profile/` - Get user profile (requires auth)
- `PUT /api/auth/profile/update/` - Update user profile (requires auth)
- `POST /api/auth/logout/` - Logout user

See **[API_DOCUMENTATION.md](./API_DOCUMENTATION.md)** for complete API reference.

## 🔐 Admin Panel

Access the admin panel at `http://localhost:8000/admin/`

Use the superuser credentials you created during setup.

**Admin Features:**
- Manage products, categories, and materials
- Review and update custom order status
- View contact messages and newsletter subscriptions
- Manage testimonials

## 🚂 Deployment

### Supabase + Railway (Recommended)

This project is configured to use **Supabase PostgreSQL** with **Railway** for hosting.

**Quick Deploy:**
1. Create Supabase project and get database URLs
2. Deploy to Railway from GitHub
3. Set environment variables in Railway
4. Your API is live!

**📖 Complete deployment guide**: See **[SUPABASE_RAILWAY_DEPLOYMENT.md](./SUPABASE_RAILWAY_DEPLOYMENT.md)**

### Alternative: Railway with Built-in PostgreSQL

If you prefer Railway's built-in database:

1. **Install Railway CLI**
```bash
npm install -g @railway/cli
```

2. **Login and Deploy**
```bash
railway login
railway init
```

3. **Add PostgreSQL**
- In Railway dashboard: New → Database → PostgreSQL
- Railway automatically sets `DATABASE_URL`

4. **Deploy**
```bash
railway up
```

### 5. Set environment variables

In Railway dashboard, add these variables:

```
SECRET_KEY=<generate-a-secret-key>
DEBUG=False
ALLOWED_HOSTS=your-railway-domain.railway.app
CORS_ALLOWED_ORIGINS=https://printbox3d.com,https://www.printbox3d.com
DATABASE_URL=<automatically-set-by-railway>
```

### 6. Deploy

```bash
railway up
```

### 7. Run migrations on Railway

```bash
railway run python manage.py migrate
railway run python manage.py createsuperuser
```

## 📁 Project Structure

```
PrintBox-Backend/
├── printbox_backend/          # Django project settings
│   ├── settings.py           # Main settings
│   ├── urls.py              # Root URL configuration
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
├── api/                     # Main API app
│   ├── models.py           # Database models
│   ├── serializers.py      # DRF serializers
│   ├── views.py            # API views
│   ├── urls.py             # API URL routing
│   └── admin.py            # Admin configuration
├── media/                  # User uploaded files
├── staticfiles/           # Static files for production
├── requirements.txt       # Python dependencies
├── Procfile              # Railway/Heroku configuration
├── railway.json          # Railway-specific config
├── runtime.txt          # Python version
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore rules
├── manage.py           # Django management script
└── README.md          # This file
```

## 🗄️ Database Models

### Product
- name, slug, description, price
- category, material
- color, dimensions, weight
- images (up to 3)
- stock_quantity, is_available, is_featured

### Category
- name, slug, description, image

### Material
- name, description, properties

### CustomOrder
- Customer info: name, email, phone
- Order details: material, color, description, quantity, budget
- design_file (optional)
- status (PENDING, REVIEWING, QUOTED, APPROVED, IN_PRODUCTION, COMPLETED, CANCELLED)

### ContactMessage
- name, email, subject, message
- is_read, admin_notes

### Newsletter
- email, is_active, subscribed_at

### Testimonial
- name, company, rating, message, image
- is_featured

## 🔧 Configuration

### CORS Settings

Update `CORS_ALLOWED_ORIGINS` in `.env`:

```env
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://printbox3d.com
```

### Media Files

Media files are stored in `/media/` directory:
- Products: `/media/products/`
- Categories: `/media/categories/`
- Custom Orders: `/media/custom_orders/`
- Testimonials: `/media/testimonials/`

For production, consider using cloud storage (AWS S3, Cloudinary, etc.)

## 📝 Sample Data

To populate the database with sample data:

```bash
python manage.py shell
```

Then run:

```python
from api.models import Category, Material, Product

# Create categories
category = Category.objects.create(
    name="Home Decor",
    description="Decorative items for your home"
)

# Create materials
material = Material.objects.create(
    name="PLA",
    description="Standard 3D printing material"
)

# Create products
Product.objects.create(
    name="Geometric Planter",
    description="Modern planter for small plants",
    price=899,
    category=category,
    material=material,
    is_available=True,
    is_featured=True,
    stock_quantity=10
)
```

## 🧪 Testing

Run tests:

```bash
python manage.py test
```

## 📧 Email Configuration

To enable email notifications, add to `.env`:

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-app-password
```

## 🔒 Security Notes

- Never commit `.env` file
- Use strong `SECRET_KEY` in production
- Set `DEBUG=False` in production
- Configure proper `ALLOWED_HOSTS`
- Use HTTPS in production
- Regularly update dependencies

## 🤝 Integration with Frontend

Update your React frontend to use the API:

```javascript
// In your React app
const API_URL = 'https://your-railway-domain.railway.app/api';

// Fetch products
fetch(`${API_URL}/products/`)
  .then(res => res.json())
  .then(data => console.log(data));

// Submit custom order
const formData = new FormData();
formData.append('name', 'John Doe');
formData.append('email', 'john@example.com');
// ... add other fields

fetch(`${API_URL}/custom-orders/`, {
  method: 'POST',
  body: formData
})
  .then(res => res.json())
  .then(data => console.log(data));
```

## 📞 Support

For issues or questions:
- Email: info@printbox3d.com
- GitHub Issues: [Create an issue](https://github.com/yourusername/printbox-backend/issues)

## 📄 License

This project is licensed under the MIT License.

---

**Built with ❤️ for PrintBox3D**
