# 🚀 Complete Setup & Testing Guide

## Quick Setup (5 Minutes)

### Prerequisites
- Python 3.11+ installed
- Git installed
- Text editor/IDE (VS Code recommended)

### Step 1: Setup Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run Setup Script

```bash
python setup.py
```

This will:
- Create `.env` file with secret key
- Run database migrations
- Optionally load sample data
- Optionally create superuser
- Collect static files

### Step 4: Start Server

```bash
python manage.py runserver
```

✅ **Done!** Your API is running at `http://localhost:8000/api/`

---

## Manual Setup (If setup.py doesn't work)

### 1. Create .env file

```env
SECRET_KEY=your-secret-key-here-change-this
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

### 2. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create superuser

```bash
python manage.py createsuperuser
```

### 4. Load sample data

```bash
python manage.py populate_sample_data
```

### 5. Start server

```bash
python manage.py runserver
```

---

## 🧪 Testing Your API

### Test 1: Check API Root

Open browser: `http://localhost:8000/api/`

You should see a browsable API interface.

### Test 2: Get Products

```bash
curl http://localhost:8000/api/products/
```

Expected response:
```json
{
  "count": 9,
  "next": null,
  "previous": null,
  "results": [...]
}
```

### Test 3: Get Featured Products

```bash
curl http://localhost:8000/api/products/featured/
```

### Test 4: Filter Products by Category

```bash
curl "http://localhost:8000/api/products/?category__slug=home-decor"
```

### Test 5: Search Products

```bash
curl "http://localhost:8000/api/products/?search=planter"
```

### Test 6: Submit Custom Order

Create a file `test_order.json`:
```json
{
  "name": "Test User",
  "email": "test@example.com",
  "phone": "+91 1234567890",
  "material": "PLA",
  "color": "Blue",
  "description": "Test custom order",
  "quantity": 1,
  "budget": "1000-2000"
}
```

Submit:
```bash
curl -X POST http://localhost:8000/api/custom-orders/ \
  -H "Content-Type: application/json" \
  -d @test_order.json
```

### Test 7: Submit Contact Message

```bash
curl -X POST http://localhost:8000/api/contact/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "subject": "Test Subject",
    "message": "Test message"
  }'
```

### Test 8: Newsletter Subscription

```bash
curl -X POST http://localhost:8000/api/newsletter/ \
  -H "Content-Type: application/json" \
  -d '{"email": "newsletter@example.com"}'
```

---

## 🖥️ Admin Panel Testing

### 1. Access Admin Panel

Open browser: `http://localhost:8000/admin/`

Login with superuser credentials.

### 2. Test Product Management

1. Go to "Products"
2. Click "Add Product"
3. Fill in details:
   - Name: Test Product
   - Category: Select one
   - Material: Select one
   - Price: 999
   - Description: Test description
   - Stock: 10
   - Check "Is available"
4. Click "Save"

### 3. Test Custom Order Management

1. Go to "Custom Orders"
2. Find test order you created
3. Change status to "REVIEWING"
4. Add admin notes
5. Save

### 4. Test Contact Messages

1. Go to "Contact Messages"
2. Mark a message as "Read"
3. Add admin notes

---

## 🔄 Integration Testing with Frontend

### 1. Start Backend

```bash
python manage.py runserver
```

### 2. Test CORS

Create a simple HTML file `test_cors.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>CORS Test</title>
</head>
<body>
    <button onclick="testAPI()">Test API</button>
    <div id="result"></div>

    <script>
        async function testAPI() {
            try {
                const response = await fetch('http://localhost:8000/api/products/');
                const data = await response.json();
                document.getElementById('result').innerHTML = 
                    `Success! Found ${data.count} products`;
            } catch (error) {
                document.getElementById('result').innerHTML = 
                    `Error: ${error.message}`;
            }
        }
    </script>
</body>
</html>
```

Open in browser and click "Test API" button.

---

## 🧪 Run Unit Tests

```bash
# Run all tests
python manage.py test

# Run specific test class
python manage.py test api.tests.ProductAPITest

# Run with verbosity
python manage.py test --verbosity=2
```

Expected output:
```
Creating test database...
........
----------------------------------------------------------------------
Ran 8 tests in 0.123s

OK
Destroying test database...
```

---

## 📊 Database Inspection

### Using Django Shell

```bash
python manage.py shell
```

Then:
```python
from api.models import Product, Category, CustomOrder

# Count products
Product.objects.count()
# Output: 9

# Get all categories
for cat in Category.objects.all():
    print(f"{cat.name}: {cat.products.count()} products")

# Get featured products
Product.objects.filter(is_featured=True).count()

# Get recent custom orders
CustomOrder.objects.all()[:5]
```

### Using DB Browser (Optional)

Install DB Browser for SQLite: https://sqlitebrowser.org/

Open `db.sqlite3` file to inspect database directly.

---

## 🔍 Debugging Tips

### Check Server Logs

Watch the terminal running `python manage.py runserver` for:
- HTTP requests
- Error messages
- SQL queries (with DEBUG=True)

### Enable Debug Mode

In `.env`:
```env
DEBUG=True
```

This shows detailed error pages.

### Check Migrations

```bash
python manage.py showmigrations
```

All migrations should have [X] checkmarks.

### Verify Static Files

```bash
python manage.py collectstatic --dry-run
```

---

## 🌐 Testing Production Setup (Before Deploy)

### 1. Set Production Settings

Create `.env.production`:
```env
SECRET_KEY=<strong-secret-key>
DEBUG=False
ALLOWED_HOSTS=.railway.app,printbox3d.com
DATABASE_URL=<postgresql-url>
CORS_ALLOWED_ORIGINS=https://printbox3d.com
```

### 2. Test with Production Settings

```bash
# Use production env
export $(cat .env.production | xargs)  # Linux/Mac
# Or manually set in Windows

# Run checks
python manage.py check --deploy

# Collect static files
python manage.py collectstatic

# Test with gunicorn
gunicorn printbox_backend.wsgi
```

---

## ✅ Pre-Deployment Checklist

### Code Quality
- [ ] All tests passing
- [ ] No TODO comments in production code
- [ ] Proper error handling
- [ ] Validation on all forms

### Security
- [ ] Strong SECRET_KEY
- [ ] DEBUG=False for production
- [ ] ALLOWED_HOSTS configured
- [ ] CORS origins specified
- [ ] No sensitive data in code

### Database
- [ ] Migrations created
- [ ] Migrations work on fresh database
- [ ] Sample data script works
- [ ] No hardcoded database credentials

### API
- [ ] All endpoints working
- [ ] Proper status codes returned
- [ ] Error messages are user-friendly
- [ ] File uploads working
- [ ] Pagination working

### Documentation
- [ ] README complete
- [ ] API documentation accurate
- [ ] Deployment guide ready
- [ ] Frontend integration guide ready

### Performance
- [ ] Database queries optimized
- [ ] Static files configured
- [ ] Media files handling setup
- [ ] WSGI server (gunicorn) configured

---

## 🚀 Ready to Deploy?

Follow `DEPLOYMENT.md` for Railway deployment.

### Quick Deploy Steps:

1. Push to GitHub
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. Connect to Railway
```bash
railway login
railway init
railway up
```

3. Add PostgreSQL
- In Railway dashboard
- Add PostgreSQL database

4. Set environment variables
- In Railway settings
- Copy from `.env.production`

5. Run migrations
```bash
railway run python manage.py migrate
railway run python manage.py createsuperuser
```

6. Done! 🎉

---

## 🆘 Common Issues & Solutions

### Issue: ModuleNotFoundError
**Solution**: 
```bash
pip install -r requirements.txt
```

### Issue: Database is locked
**Solution**:
```bash
# Close all connections to database
# Delete db.sqlite3
rm db.sqlite3
python manage.py migrate
```

### Issue: Static files not found
**Solution**:
```bash
python manage.py collectstatic --clear --noinput
```

### Issue: CORS errors in browser
**Solution**: Check `.env` has correct frontend URL:
```env
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

### Issue: File upload fails
**Solution**: Check `media/` directory exists and is writable

### Issue: Can't create superuser
**Solution**: Make sure migrations are run first:
```bash
python manage.py migrate
python manage.py createsuperuser
```

---

## 📞 Getting Help

1. **Check Documentation**
   - README.md
   - API_DOCUMENTATION.md
   - DEPLOYMENT.md

2. **Django Docs**
   - https://docs.djangoproject.com

3. **DRF Docs**
   - https://www.django-rest-framework.org

4. **Create GitHub Issue**
   - Include error message
   - Include steps to reproduce
   - Include environment details

---

## 🎓 Learning Resources

- Django Tutorial: https://docs.djangoproject.com/en/4.2/intro/tutorial01/
- DRF Tutorial: https://www.django-rest-framework.org/tutorial/quickstart/
- Python Virtual Environments: https://docs.python.org/3/tutorial/venv.html
- REST API Best Practices: https://restfulapi.net/

---

**You're all set! Happy coding! 🎉**
