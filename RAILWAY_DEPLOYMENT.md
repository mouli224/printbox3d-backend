# Railway Deployment Guide for PrintBox3D Backend

## Required Environment Variables for Railway

Add these environment variables in your Railway project settings:

### Django Settings
```
DEBUG=False
SECRET_KEY=your-super-secret-key-change-this-in-production
ALLOWED_HOSTS=your-domain.railway.app,www.printbox3d.com,printbox3d.com
```

### Database (Railway provides PostgreSQL)
```
DATABASE_URL=postgresql://user:password@host:port/dbname
```
(Railway automatically provides this if you add PostgreSQL service)

### CORS Settings (Important!)
```
CORS_ALLOWED_ORIGINS=https://printbox3d.vercel.app,https://www.printbox3d.com,https://printbox3d.com
```

### Email Configuration (Gmail)
```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=info@printbox3d.com
EMAIL_HOST_PASSWORD=your-app-specific-password
DEFAULT_FROM_EMAIL=PrintBox3D <info@printbox3d.com>
```

**Important for Gmail:**
1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password: https://myaccount.google.com/apppasswords
3. Use the App Password (16-character code) as EMAIL_HOST_PASSWORD

### Razorpay Payment Gateway
```
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret
```

### Media Files (Static Files)
```
STATIC_URL=/static/
MEDIA_URL=/media/
```

## Deployment Steps

### 1. Connect GitHub Repository
- Go to Railway dashboard
- Click "New Project" → "Deploy from GitHub repo"
- Select your `printbox3d-backend` repository

### 2. Add PostgreSQL Database
- In your Railway project, click "New"
- Select "Database" → "Add PostgreSQL"
- Railway will automatically set DATABASE_URL

### 3. Configure Environment Variables
- Go to your backend service → Variables
- Add all the environment variables listed above
- Make sure to replace placeholder values

### 4. Update Frontend Environment Variable (Vercel)
In your Vercel project settings, add:
```
REACT_APP_API_URL=https://your-railway-backend.railway.app
```

### 5. Deploy
- Railway will automatically deploy when you push to GitHub
- Check the deployment logs for any errors

## Important Configuration Changes

### 1. Update settings.py for Production
The settings.py already handles environment variables, but verify:

```python
# CORS Configuration
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')

# Static and Media Files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### 2. Database Migration
After deployment, run migrations in Railway console:
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 3. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

## Testing the Deployment

1. Check backend health: `https://your-railway-backend.railway.app/api/products/`
2. Test frontend connection from Vercel
3. Try placing a test order
4. Verify email notifications are working

## Troubleshooting

### CORS Errors
- Verify CORS_ALLOWED_ORIGINS includes your Vercel domain
- Check that both domains (with and without www) are included

### Database Connection Issues
- Ensure PostgreSQL service is running
- Check DATABASE_URL is correctly set

### Email Not Sending
- Verify Gmail App Password is correct
- Check EMAIL_HOST_USER and EMAIL_HOST_PASSWORD
- Ensure 2FA is enabled on Gmail account

### Static Files Not Loading
- Run `python manage.py collectstatic`
- Verify STATIC_ROOT and STATIC_URL settings

## Post-Deployment Checklist

- [ ] Backend accessible at Railway URL
- [ ] Database migrations completed
- [ ] Admin panel accessible
- [ ] Frontend can connect to backend
- [ ] Products loading correctly
- [ ] Cart functionality working
- [ ] Checkout process functional
- [ ] Email notifications sending
- [ ] Payment gateway testing (use test mode first)

## Railway CLI (Optional)

Install Railway CLI for easier management:
```bash
npm i -g @railway/cli
railway login
railway link
railway run python manage.py migrate
```

## Support

For issues:
- Check Railway logs: Railway Dashboard → Your Service → Logs
- Check Vercel logs for frontend issues
- Test backend endpoints directly using Postman or curl
