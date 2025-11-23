# Railway Deployment Guide for PrintBox Backend

## Prerequisites
- Railway account (sign up at https://railway.app)
- GitHub account with your backend code pushed
- Supabase PostgreSQL database credentials

## Step-by-Step Railway Setup

### 1. Create New Railway Project

1. Go to https://railway.app/dashboard
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your repository: `printbox3d-backend`
5. Railway will automatically detect it's a Python/Django project

### 2. Configure Environment Variables

In your Railway project dashboard:

1. Click on your service
2. Go to the **"Variables"** tab
3. Click **"Add Variable"** and add the following:

#### Required Environment Variables:

```bash
# Database Configuration (Supabase)
DATABASE_URL=postgresql://postgres.mnnkthouavmpcycsvpog:Printbox3d%40406@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres

DIRECT_DATABASE_URL=postgresql://postgres.mnnkthouavmpcycsvpog:Printbox3d%40406@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres

# Django Secret Key (generate a new one)
SECRET_KEY=y%2wi!$m=l!vxc78fj0k6yq8)#09^3gvddo^n_dpo*v8uo!u8@

# Debug Mode (always False in production)
DEBUG=False

# Allowed Hosts (Railway will provide the domain)
ALLOWED_HOSTS=*.railway.app,printbox3d.com,www.printbox3d.com

# Python Version
PYTHON_VERSION=3.11.0
```

**Important Notes:**
- Remove `?pgbouncer=true` from DATABASE_URL if present
- The `%40` in the URL is the URL-encoded `@` from your password
- Railway automatically provides `PORT` variable, no need to add it

### 3. Configure Build Settings

Railway should auto-detect these from your files:
- **Build Command**: Automatic (uses `requirements.txt`)
- **Start Command**: Automatic (uses `Procfile`)

If needed, you can manually set:
- **Start Command**: `gunicorn printbox_backend.wsgi --log-file -`

### 4. Run Database Migrations

After deployment, you need to run migrations:

1. In Railway dashboard, click on your service
2. Go to **"Settings"** tab
3. Find **"Service"** section
4. Click on **"New Deployment"** (or wait for automatic deployment)
5. Once deployed, go to **"Deployments"** tab
6. Click on the latest deployment
7. Click **"View Logs"** to monitor the deployment

To run migrations manually:
1. Install Railway CLI: `npm install -g @railway/cli`
2. Login: `railway login`
3. Link project: `railway link`
4. Run migrations: `railway run python manage.py migrate`

### 5. Collect Static Files

Static files are automatically collected during deployment due to the build process.

If you need to run it manually:
```bash
railway run python manage.py collectstatic --noinput
```

### 6. Create Superuser (Optional)

To access Django admin:
```bash
railway run python manage.py createsuperuser
```

Or add this to your Railway variables and it will auto-create:
```bash
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@printbox3d.com
DJANGO_SUPERUSER_PASSWORD=YourSecurePassword123
```

Then add this management command to run on deployment.

### 7. Get Your Railway URL

After deployment:
1. Go to your service in Railway dashboard
2. Click **"Settings"** tab
3. Scroll to **"Domains"** section
4. You'll see your Railway URL (e.g., `web-production-xxxx.up.railway.app`)
5. You can also add a custom domain here

### 8. Update Frontend Configuration

Once you have your Railway URL, update your frontend:

**For Vercel/Netlify:**
1. Go to your hosting platform dashboard
2. Find your project settings
3. Add environment variable:
   ```
   REACT_APP_API_URL=https://your-railway-url.up.railway.app
   ```
4. Redeploy your frontend

### 9. Verify Deployment

Test your API endpoints:

1. **Health Check**: `https://your-railway-url.up.railway.app/`
2. **Products API**: `https://your-railway-url.up.railway.app/api/products/`
3. **Categories API**: `https://your-railway-url.up.railway.app/api/categories/`
4. **Admin Panel**: `https://your-railway-url.up.railway.app/admin/`

## Troubleshooting

### Issue: 502 Bad Gateway

**Causes:**
- Missing environment variables
- Database connection failed
- Application crashed during startup

**Solutions:**
1. Check deployment logs in Railway dashboard
2. Verify all environment variables are set correctly
3. Ensure DATABASE_URL doesn't have `?pgbouncer=true` parameter
4. Check if Supabase database is accessible

### Issue: Database Connection Error

**Error**: `invalid dsn: invalid connection option "pgbouncer"`

**Solution:**
Remove `?pgbouncer=true` from your DATABASE_URL:
```
# WRONG
postgresql://...@....supabase.com:6543/postgres?pgbouncer=true

# CORRECT
postgresql://...@....supabase.com:6543/postgres
```

### Issue: CORS Errors

**Error**: `No 'Access-Control-Allow-Origin' header`

**Solution:**
Your backend is already configured with the correct CORS origins:
- https://printbox3d.com
- https://www.printbox3d.com

Make sure your frontend is using the correct Railway backend URL.

### Issue: Static Files Not Loading

**Solution:**
Railway automatically collects static files during build. If you have issues:

1. Check your `settings.py`:
   ```python
   STATIC_ROOT = BASE_DIR / 'staticfiles'
   STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
   ```

2. Verify `whitenoise` is in `requirements.txt`

3. Check middleware order in `settings.py` (WhiteNoise should be after SecurityMiddleware)

### Issue: Migration Errors

**Error**: Connection pooling issues during migrations

**Solution:**
Use `DIRECT_DATABASE_URL` (port 5432) which bypasses PgBouncer:
```bash
railway run python manage.py migrate
```

## Monitoring and Logs

### View Real-Time Logs:
1. Go to Railway dashboard
2. Click on your service
3. Click **"Deployments"** tab
4. Click on latest deployment
5. View logs in real-time

### Check Service Metrics:
1. Railway provides CPU, Memory, and Network usage
2. Monitor under **"Metrics"** tab

## Updating Your Deployment

### Automatic Deployments (Recommended):
1. Push changes to your GitHub repository:
   ```bash
   git add .
   git commit -m "Your changes"
   git push origin main
   ```
2. Railway automatically detects changes and redeploys

### Manual Deployment:
1. Use Railway CLI:
   ```bash
   railway up
   ```

## Security Checklist

- ✅ `DEBUG=False` in production
- ✅ Strong `SECRET_KEY` (generated randomly)
- ✅ Database credentials are URL-encoded
- ✅ CORS origins explicitly listed (no wildcards)
- ✅ HTTPS enforced for production domains
- ✅ `.env` files excluded from git
- ✅ Sensitive data in Railway environment variables only

## Backup and Database Management

### Database Backup:
```bash
# Using Railway CLI
railway run python manage.py dumpdata > backup.json
```

### Database Restore:
```bash
railway run python manage.py loaddata backup.json
```

### Run Django Shell:
```bash
railway run python manage.py shell
```

## Cost Optimization

Railway provides:
- **$5 free credit** per month
- **500 hours** of execution time on free plan

Tips:
1. Remove unused services
2. Monitor usage in billing dashboard
3. Set up spending limits

## Support

- **Railway Docs**: https://docs.railway.app
- **Railway Discord**: https://discord.gg/railway
- **Django Deployment**: https://docs.djangoproject.com/en/4.2/howto/deployment/

## Quick Command Reference

```bash
# Railway CLI Commands
railway login                          # Login to Railway
railway link                          # Link to existing project
railway run python manage.py migrate  # Run migrations
railway run python manage.py shell    # Open Django shell
railway logs                          # View logs
railway status                        # Check service status
railway open                          # Open Railway dashboard
```

---

**Your Backend Configuration Summary:**

- **Repository**: github.com/mouli224/printbox3d-backend
- **Database**: Supabase PostgreSQL (AWS Singapore)
- **Frontend Domains**: printbox3d.com, www.printbox3d.com
- **CORS**: Configured for production domains
- **Static Files**: Handled by WhiteNoise
- **Web Server**: Gunicorn

After following this guide, your backend will be fully deployed and ready to serve your frontend! 🚀
