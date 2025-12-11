# PrintBox3D Backend

Django REST API for PrintBox3D - A 3D printing e-commerce platform with Razorpay payment integration.

---

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Features](#-features)
- [Environment Setup](#-environment-setup)
- [Database Configuration](#-database-configuration)
- [API Endpoints](#-api-endpoints)
- [Payment Integration](#-payment-integration)
- [Deployment](#-deployment)
- [Utility Scripts](#-utility-scripts)
- [Troubleshooting](#-troubleshooting)

---

## 🚀 Quick Start

### Local Development Setup

```bash
# Clone repository
git clone https://github.com/mouli224/printbox3d-backend.git
cd printbox3d-backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your credentials (see Environment Setup section)

# Run migrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser

# Add sample products (optional)
python scripts/add_products.py

# Start development server
python manage.py runserver
```

Visit:
- **API**: http://localhost:8000/api/
- **Admin**: http://localhost:8000/admin/

---

## 📁 Project Structure

```
printbox_backend/
├── api/                      # Main Django app
│   ├── models.py            # Database models (Product, Order, Payment, etc.)
│   ├── views.py             # API endpoints and business logic
│   ├── serializers.py       # Data serialization for API responses
│   ├── urls.py              # URL routing
│   ├── auth_views.py        # JWT authentication endpoints
│   ├── email_utils.py       # Email notification functions
│   └── migrations/          # Database migrations
├── printbox_backend/         # Django project settings
│   ├── settings.py          # Main configuration
│   ├── urls.py              # Root URL configuration
│   └── wsgi.py              # WSGI application
├── scripts/                  # Utility scripts
│   ├── add_products.py      # Populate product catalog
│   ├── add_test_product.py  # Add ₹1 test product
│   ├── check_env.py         # Verify environment variables
│   └── generate_secret_key.py # Generate Django SECRET_KEY
├── media/                    # User-uploaded files
├── docs/                     # Additional documentation
├── .env                      # Environment variables (not in git)
├── .env.example              # Environment template
├── requirements.txt          # Python dependencies
├── manage.py                 # Django management script
├── Procfile                  # Railway deployment config
└── README.md                 # This file
```

---

## 🔑 Features

### Product Management
- Product catalog with categories and materials
- Product search and filtering
- Featured products
- Stock management
- Image uploads

### E-commerce
- Shopping cart (session-based and user-linked)
- Order creation and tracking
- Order history for authenticated users
- Custom order requests (file uploads)

### Payment Processing
- **Razorpay** payment gateway integration
- Secure payment signature verification
- Automatic stock updates after payment
- Order confirmation emails

### User Management
- JWT-based authentication
- User registration and login
- Password reset functionality
- User profile management

### Additional Features
- Contact form with email notifications
- Newsletter subscriptions
- Customer testimonials
- Admin dashboard (Django Admin)

---

## 🛠️ Environment Setup

### Required Environment Variables

Create `.env` file in project root with these variables:

```env
# ==================== DJANGO CORE ====================
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Generate SECRET_KEY:
# python scripts/generate_secret_key.py

# ==================== DATABASE ====================
# For local development (uses SQLite): leave empty
DATABASE_URL=

# For production (Supabase PostgreSQL):
# DATABASE_URL=postgresql://user:password@host:6543/postgres
# DIRECT_DATABASE_URL=postgresql://user:password@host:5432/postgres

# ==================== PAYMENT GATEWAY ====================
# Razorpay LIVE credentials (production)
RAZORPAY_KEY_ID=rzp_live_xxx
RAZORPAY_KEY_SECRET=xxx

# Razorpay TEST credentials (development)
# RAZORPAY_KEY_ID=rzp_test_xxx
# RAZORPAY_KEY_SECRET=xxx

# ==================== CORS & SECURITY ====================
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://www.printbox3d.com
CSRF_TRUSTED_ORIGINS=http://localhost:8000,https://your-backend-domain.com

# ==================== EMAIL (Optional) ====================
EMAIL_HOST=smtp.hostinger.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=info@printbox3d.com
EMAIL_HOST_PASSWORD=your-email-password
DEFAULT_FROM_EMAIL=info@printbox3d.com
```

### Environment Variables Explained

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | ✅ Yes | Django secret key (generate with `scripts/generate_secret_key.py`) |
| `DEBUG` | No | `True` for development, **`False`** for production |
| `ALLOWED_HOSTS` | No | Comma-separated domains (e.g., `localhost,yourdomain.com`) |
| `DATABASE_URL` | No | PostgreSQL URL (uses SQLite if not set) |
| `RAZORPAY_KEY_ID` | ✅ Yes | Razorpay API key from dashboard |
| `RAZORPAY_KEY_SECRET` | ✅ Yes | Razorpay API secret (keep secure!) |
| `CORS_ALLOWED_ORIGINS` | No | Frontend URLs for CORS (comma-separated) |
| `EMAIL_HOST` | No | SMTP server for email notifications |

---

## 🗄️ Database Configuration

### Local Development (SQLite)

Default setup uses SQLite - no configuration needed:

```bash
python manage.py migrate
```

Database file: `db.sqlite3`

### Production (PostgreSQL - Supabase)

1. **Create Supabase Project**: https://supabase.com
2. **Get Connection Strings** from Supabase dashboard:
   - Pooled connection (port 6543) - for app
   - Direct connection (port 5432) - for migrations

3. **Update `.env`**:
```env
DATABASE_URL=postgresql://postgres.xxx:PASSWORD@xxx.pooler.supabase.com:6543/postgres
DIRECT_DATABASE_URL=postgresql://postgres.xxx:PASSWORD@xxx.pooler.supabase.com:5432/postgres
```

4. **Run Migrations**:
```bash
python manage.py migrate
```

### Database URL Formats

**Supabase Pooled** (for runtime):
```
postgresql://postgres.xxx:PASSWORD@xxx.pooler.supabase.com:6543/postgres
```

**Supabase Direct** (for migrations):
```
postgresql://postgres.xxx:PASSWORD@xxx.pooler.supabase.com:5432/postgres
```

**Railway PostgreSQL**:
```
postgresql://postgres:PASSWORD@HOST:5432/railway
```

---

## 📡 API Endpoints

### Authentication
```
POST /api/auth/register/          - Register new user
POST /api/auth/login/             - Login (get JWT tokens)
POST /api/auth/refresh/           - Refresh access token
POST /api/auth/logout/            - Logout (blacklist token)
```

### Products
```
GET  /api/products/               - List all products (with filters)
GET  /api/products/{slug}/        - Get product details
GET  /api/products/featured/      - Get featured products
GET  /api/products/best_sellers/  - Get best sellers
```

**Query Parameters**:
- `category__slug` - Filter by category
- `material__name` - Filter by material
- `search` - Search in name/description
- `ordering` - Sort by: `price`, `-price`, `name`, `-created_at`

**Example**:
```
GET /api/products/?category__slug=home-decor&ordering=-price
```

### Categories & Materials
```
GET /api/categories/              - List all categories
GET /api/materials/               - List all materials
```

### Orders
```
POST /api/orders/create/          - Create order & initiate payment
POST /api/orders/verify-payment/  - Verify Razorpay payment
GET  /api/orders/{order_id}/      - Get order status
GET  /api/orders/user/            - Get user's order history (auth required)
POST /api/orders/payment-failed/  - Record payment failure
```

### Custom Orders
```
POST /api/custom-orders/          - Submit custom order request
```

### Contact & Newsletter
```
POST /api/contact/                - Submit contact form
POST /api/newsletter/             - Subscribe to newsletter
```

### Testimonials
```
GET /api/testimonials/            - List testimonials
GET /api/testimonials/featured/   - Get featured testimonials
```

---

## 💳 Payment Integration (Razorpay)

### Setup

1. **Get Razorpay Credentials**:
   - Sign up at https://razorpay.com
   - Go to Dashboard → Settings → API Keys
   - Generate Live/Test keys

2. **Add to `.env`**:
```env
RAZORPAY_KEY_ID=rzp_live_xxxxx
RAZORPAY_KEY_SECRET=xxxxx
```

3. **Frontend Integration**:
   - Backend provides `razorpay_key_id` in `/api/orders/create/` response
   - Frontend loads Razorpay checkout script
   - After payment, verify signature with `/api/orders/verify-payment/`

### Payment Flow

```
1. Customer adds items to cart
2. Frontend calls POST /api/orders/create/
   - Backend creates Order & Razorpay order
   - Returns razorpay_order_id, razorpay_key_id, amount
3. Frontend opens Razorpay checkout modal
4. Customer completes payment
5. Razorpay returns payment_id, order_id, signature
6. Frontend calls POST /api/orders/verify-payment/
   - Backend verifies HMAC signature
   - Updates order status to PAID
   - Reduces product stock
   - Sends confirmation email
7. Frontend redirects to success page
```

### Testing Payments

Use test product (₹1):
```bash
python scripts/add_test_product.py
```

**Test Card Details** (Razorpay Test Mode):
- Card: 4111 1111 1111 1111
- CVV: Any 3 digits
- Expiry: Any future date

---

## 🚀 Deployment

### Railway Deployment (Recommended)

#### Prerequisites
- GitHub account with code pushed
- Railway account (https://railway.app)
- Supabase PostgreSQL database

#### Steps

**1. Push to GitHub**:
```bash
git add -A
git commit -m "Ready for deployment"
git push origin main
```

**2. Create Railway Project**:
- Go to https://railway.app/dashboard
- Click "New Project" → "Deploy from GitHub repo"
- Select your `printbox3d-backend` repository

**3. Add Environment Variables** in Railway dashboard → Variables:

```bash
SECRET_KEY=<generated-secret-key>
DEBUG=False
ALLOWED_HOSTS=*.railway.app,printbox3d.com,www.printbox3d.com
DATABASE_URL=postgresql://user:pass@host:6543/postgres
RAZORPAY_KEY_ID=rzp_live_xxx
RAZORPAY_KEY_SECRET=xxx
CORS_ALLOWED_ORIGINS=https://www.printbox3d.com,https://printbox3d.com
CSRF_TRUSTED_ORIGINS=https://your-railway-domain.railway.app,https://printbox3d.com
EMAIL_HOST=smtp.hostinger.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=info@printbox3d.com
EMAIL_HOST_PASSWORD=xxx
DEFAULT_FROM_EMAIL=info@printbox3d.com
```

**4. Deploy**:
- Railway auto-deploys on every git push
- Check deployment logs for errors
- Test endpoints at your Railway URL

**5. Run Migrations** (one-time):
```bash
# In Railway shell
python manage.py migrate
python manage.py createsuperuser
```

#### Important Notes

⚠️ **Production Checklist**:
- [ ] `DEBUG=False`
- [ ] Strong `SECRET_KEY` (use `scripts/generate_secret_key.py`)
- [ ] `ALLOWED_HOSTS` includes your domain
- [ ] `CORS_ALLOWED_ORIGINS` includes frontend URL
- [ ] Razorpay **LIVE** credentials (not test)
- [ ] Email credentials configured
- [ ] Database backups enabled (Supabase)

---

## 🛠️ Utility Scripts

Scripts located in `scripts/` directory:

### Product Management

```bash
# Add full product catalog
python scripts/add_products.py

# Add test product (₹1 for payment testing)
python scripts/add_test_product.py

# Add specific new products
python scripts/add_new_products.py

# Split keychain variants
python scripts/split_keychains.py

# Add discount percentages
python scripts/add_discount.py
```

### Deployment Tools

```bash
# Generate Django SECRET_KEY
python scripts/generate_secret_key.py

# Check environment variables (run in Railway shell)
python scripts/check_env.py
```

---

## 🐛 Troubleshooting

### Common Issues

**1. Payment 502 Error / CORS Blocked**

**Problem**: `502 Bad Gateway` or `CORS policy blocked`

**Solution**:
```bash
# Check Railway environment variables are set:
RAZORPAY_KEY_ID=xxx
RAZORPAY_KEY_SECRET=xxx
CORS_ALLOWED_ORIGINS=https://www.printbox3d.com

# Verify in Railway shell:
python scripts/check_env.py
```

**2. Database Connection Error**

**Problem**: `could not connect to server` or `relation does not exist`

**Solution**:
```bash
# Verify DATABASE_URL format (must include port 6543 for pooling)
DATABASE_URL=postgresql://user:pass@host:6543/postgres

# Run migrations
python manage.py migrate
```

**3. Razorpay Signature Verification Failed**

**Problem**: Payment succeeds but verification fails

**Solution**:
- Ensure `RAZORPAY_KEY_SECRET` matches your Razorpay dashboard
- Check CORS is properly configured
- Verify frontend sends correct `razorpay_signature`

**4. Import Errors / Module Not Found**

**Problem**: `ModuleNotFoundError: No module named 'xxx'`

**Solution**:
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Verify virtual environment is activated
# Should see (.venv) in terminal prompt
```

**5. Static Files Not Loading (Production)**

**Problem**: CSS/JS not loading in admin panel

**Solution**:
```bash
# Collect static files
python manage.py collectstatic --noinput
```

### Debug Mode

**Enable detailed error messages** (development only):

```env
DEBUG=True
```

**Check Django logs**:
```bash
# Railway logs
railway logs

# Local logs
# Errors appear in terminal running manage.py runserver
```

---

## 🧪 Testing

### Run Tests
```bash
python manage.py test
```

### Test Payment Flow
```bash
# 1. Add test product
python scripts/add_test_product.py

# 2. Use Razorpay test credentials
RAZORPAY_KEY_ID=rzp_test_xxx
RAZORPAY_KEY_SECRET=xxx

# 3. Test card numbers (Razorpay Test Mode)
Card: 4111 1111 1111 1111
CVV: 123
Expiry: 12/25
```

---

## 📚 Technology Stack

- **Backend**: Django 4.2.7
- **API**: Django REST Framework
- **Authentication**: djangorestframework-simplejwt
- **Database**: PostgreSQL (Supabase) / SQLite (dev)
- **Payment**: Razorpay
- **Email**: SMTP (Hostinger)
- **Storage**: Media files (local/cloud)
- **Hosting**: Railway
- **Version Control**: Git + GitHub

---

## 📞 Support

- **Email**: info@printbox3d.com
- **Website**: https://www.printbox3d.com
- **Issues**: [GitHub Issues](https://github.com/mouli224/printbox3d-backend/issues)

---

## 📝 License

MIT License - Free to use for personal and commercial projects.

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

**Built with ❤️ for PrintBox3D**
