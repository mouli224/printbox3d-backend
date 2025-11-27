# Environment Variables Reference

Quick reference for all environment variables used in PrintBox3D Backend.

## 🔧 Django Core Settings

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | Yes | (dev key) | Django secret key for production |
| `DEBUG` | No | `False` | Enable debug mode (set to `False` in production) |
| `ALLOWED_HOSTS` | No | `localhost,127.0.0.1` | Comma-separated list of allowed hosts |

**Generate SECRET_KEY:**
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

---

## 🗄️ Database Settings

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | No | (SQLite) | PostgreSQL connection URL with pooling |
| `DIRECT_DATABASE_URL` | No | (SQLite) | Direct PostgreSQL URL for migrations |

### Database URL Format

**Supabase Connection Pooling (Port 6543):**
```
postgresql://postgres.xxx:PASSWORD@xxx.pooler.supabase.com:6543/postgres
```

**Supabase Direct Connection (Port 5432):**
```
postgresql://postgres.xxx:PASSWORD@xxx.pooler.supabase.com:5432/postgres
```

**Railway PostgreSQL:**
```
postgresql://user:password@host:port/database
```

### When to Use Which?

| Operation | Uses | Reason |
|-----------|------|--------|
| `python manage.py runserver` | `DATABASE_URL` | Connection pooling for performance |
| `python manage.py migrate` | `DIRECT_DATABASE_URL` | Bypasses pooler for compatibility |
| Normal API requests | `DATABASE_URL` | Efficient connection reuse |

---

## 🌐 CORS Settings

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `CORS_ALLOWED_ORIGINS` | No | `http://localhost:3000` | Comma-separated list of allowed origins |

**Example:**
```env
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://printbox3d.com,https://www.printbox3d.com
```

---

## 📧 Email Settings

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `EMAIL_HOST` | No | `smtp.gmail.com` | SMTP server hostname |
| `EMAIL_PORT` | No | `587` | SMTP server port |
| `EMAIL_USE_TLS` | No | `True` | Use TLS encryption |
| `EMAIL_HOST_USER` | No | - | Email account username |
| `EMAIL_HOST_PASSWORD` | No | - | Email account password |
| `DEFAULT_FROM_EMAIL` | No | `noreply@printbox3d.com` | Default sender email |

**Gmail Setup:**
1. Enable 2-factor authentication
2. Generate app-specific password
3. Use app password in `EMAIL_HOST_PASSWORD`

---

## 🔑 JWT Settings

JWT settings are configured in `settings.py`:

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}
```

No environment variables needed for JWT configuration.

---

## 💳 Razorpay Payment Settings

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `RAZORPAY_KEY_ID` | Yes | - | Razorpay API Key ID |
| `RAZORPAY_KEY_SECRET` | Yes | - | Razorpay API Key Secret |

**How to Get Razorpay Keys:**
1. Sign up at [razorpay.com](https://razorpay.com)
2. Complete KYC verification
3. Go to Settings → API Keys
4. Generate Test Mode keys for development
5. Generate Live Mode keys for production

**Example:**
```env
# Test Mode (Development)
RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxxxx
RAZORPAY_KEY_SECRET=xxxxxxxxxxxxxxxxxxxxxxxx

# Live Mode (Production)
RAZORPAY_KEY_ID=rzp_live_xxxxxxxxxxxxxx
RAZORPAY_KEY_SECRET=xxxxxxxxxxxxxxxxxxxxxxxx
```

**⚠️ Important:**
- Test mode keys work with test card numbers only
- Live mode keys process real payments
- Never commit keys to Git
- Keep SECRET separate from KEY_ID

---

## 📝 Example Configurations

### Local Development

```env
# .env
SECRET_KEY=your-dev-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
# DATABASE_URL is empty - uses SQLite
```

### Production (Supabase + Railway)

```env
# Railway Environment Variables
SECRET_KEY=prod-secret-key-50-chars-long-xxxxxxxxxxxxxxxxxx
DEBUG=False
ALLOWED_HOSTS=api.printbox3d.com,printbox3d-backend.railway.app

DATABASE_URL=postgresql://postgres.mnnkthouavmpcycsvpog:PASSWORD@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres

DIRECT_DATABASE_URL=postgresql://postgres.mnnkthouavmpcycsvpog:PASSWORD@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres

CORS_ALLOWED_ORIGINS=https://printbox3d.com,https://www.printbox3d.com

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=noreply@printbox3d.com
EMAIL_HOST_PASSWORD=your-app-specific-password

RAZORPAY_KEY_ID=rzp_live_xxxxxxxxxxxxxx
RAZORPAY_KEY_SECRET=xxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 🛡️ Security Best Practices

### Production Checklist

- [ ] `DEBUG=False`
- [ ] Strong `SECRET_KEY` (minimum 50 characters)
- [ ] `ALLOWED_HOSTS` limited to your domains only
- [ ] `CORS_ALLOWED_ORIGINS` limited to trusted domains
- [ ] Database credentials are strong and unique
- [ ] Email password uses app-specific password
- [ ] Environment variables stored securely (not in code)
- [ ] `.env` file is in `.gitignore`

### Environment Variable Security

**❌ Don't:**
- Commit `.env` file to Git
- Use weak or default passwords
- Share credentials in code or documentation
- Use `DEBUG=True` in production
- Allow `*` in ALLOWED_HOSTS or CORS

**✅ Do:**
- Use `.env.example` as a template (no secrets)
- Generate strong random keys
- Use Railway's environment variable protection
- Rotate credentials regularly
- Use different credentials for dev/staging/prod

---

## 🔄 Updating Variables

### Local Development
1. Edit `.env` file
2. Restart Django server: `python manage.py runserver`

### Railway
1. Go to Railway dashboard
2. Select your service
3. Click "Variables" tab
4. Add/edit variables
5. Railway automatically redeploys

### Using Railway CLI
```bash
# Set a variable
railway variables set SECRET_KEY="your-secret-key"

# View all variables
railway variables

# Delete a variable
railway variables delete VARIABLE_NAME
```

---

## 🧪 Testing Configuration

Test your environment setup:

```python
# In Django shell
python manage.py shell

# Check settings
from django.conf import settings
print(f"DEBUG: {settings.DEBUG}")
print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
print(f"Database: {settings.DATABASES['default']['ENGINE']}")
print(f"CORS Origins: {settings.CORS_ALLOWED_ORIGINS}")
```

---

## 📚 Related Documentation

- **[SUPABASE_RAILWAY_DEPLOYMENT.md](./SUPABASE_RAILWAY_DEPLOYMENT.md)** - Complete deployment guide
- **[README.md](./README.md)** - Project overview and setup
- **[API_DOCUMENTATION.md](./API_DOCUMENTATION.md)** - API reference

---

**Last Updated:** November 2025
