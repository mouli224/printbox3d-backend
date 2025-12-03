# Environment Variables Quick Reference

## Railway (Backend) - Copy these to Railway Variables

```bash
# Django Core
DEBUG=False
SECRET_KEY=django-insecure-change-this-to-random-50-character-string
ALLOWED_HOSTS=printbox3d-backend.railway.app,www.printbox3d.com,printbox3d.com

# CORS (Replace with your actual Vercel domain)
CORS_ALLOWED_ORIGINS=https://printbox3d.vercel.app,https://www.printbox3d.com,https://printbox3d.com

# Email (Gmail)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=info@printbox3d.com
EMAIL_HOST_PASSWORD=your-16-char-app-password-here
DEFAULT_FROM_EMAIL=PrintBox3D <info@printbox3d.com>

# Razorpay
RAZORPAY_KEY_ID=rzp_test_your_key_id
RAZORPAY_KEY_SECRET=your_razorpay_secret

# Database (Railway auto-provides this)
DATABASE_URL=postgresql://...
```

## Vercel (Frontend) - Add in Vercel Project Settings → Environment Variables

```bash
# Backend API URL (Replace with your Railway backend URL)
REACT_APP_API_URL=https://printbox3d-backend.railway.app
```

## How to Get Gmail App Password

1. Go to https://myaccount.google.com/
2. Security → 2-Step Verification (enable if not enabled)
3. Scroll down → App passwords
4. Select app: "Mail", Select device: "Other"
5. Enter name: "PrintBox3D Backend"
6. Copy the 16-character password
7. Use this as EMAIL_HOST_PASSWORD in Railway

## How to Find Your Railway Backend URL

1. Go to Railway Dashboard
2. Click on your backend service
3. Go to Settings → Domains
4. Copy the `.railway.app` domain
5. Use this as REACT_APP_API_URL in Vercel (with https://)

## Testing After Deployment

1. Backend: `https://your-backend.railway.app/api/products/`
2. Frontend: `https://your-frontend.vercel.app`
3. Place test order to verify email notifications
