# Supabase + Railway Deployment Guide

This guide explains how to deploy the PrintBox3D backend to Railway using Supabase PostgreSQL database.

## Prerequisites

1. **Supabase Account**: Sign up at https://supabase.com
2. **Railway Account**: Sign up at https://railway.app
3. **GitHub Repository**: Push your code to GitHub

## Step 1: Set Up Supabase Database

### 1.1 Create a New Project
1. Go to https://app.supabase.com
2. Click "New Project"
3. Choose your organization
4. Enter project details:
   - **Name**: `printbox3d-db`
   - **Database Password**: Use a strong password (save this!)
   - **Region**: Choose closest to your users (e.g., Southeast Asia)

### 1.2 Get Database URLs
1. Go to your project dashboard
2. Click on "Project Settings" (gear icon)
3. Navigate to "Database" section
4. You'll see:
   - **Connection pooling URL** (Port 6543) - for application connections
   - **Direct connection URL** (Port 5432) - for migrations

Your URLs should look like:
```
# Connection Pooling (for app)
postgresql://postgres.mnnkthouavmpcycsvpog:[YOUR-PASSWORD]@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres?pgbouncer=true

# Direct Connection (for migrations)
postgresql://postgres.mnnkthouavmpcycsvpog:[YOUR-PASSWORD]@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres
```

## Step 2: Configure Local Environment

### 2.1 Update .env File
Replace `[YOUR-PASSWORD]` with your actual Supabase database password:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DATABASE_URL=postgresql://postgres.mnnkthouavmpcycsvpog:YOUR_ACTUAL_PASSWORD@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres?pgbouncer=true

# Direct database connection (used for migrations)
DIRECT_DATABASE_URL=postgresql://postgres.mnnkthouavmpcycsvpog:YOUR_ACTUAL_PASSWORD@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://printbox3d.com
```

### 2.2 Test Local Connection
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

If migrations fail, ensure:
- Database password is correct
- Your IP is allowed in Supabase (check Network Restrictions)

## Step 3: Deploy to Railway

### 3.1 Create New Railway Project
1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Connect your GitHub account
5. Select your `PrintBox-Backend` repository

### 3.2 Configure Environment Variables

Click on your service → Variables → Add these:

#### Required Variables:
```env
SECRET_KEY=your-production-secret-key-generate-a-new-one
DEBUG=False
ALLOWED_HOSTS=your-app-name.railway.app,printbox3d.com,www.printbox3d.com

# Database URLs (from Supabase)
DATABASE_URL=postgresql://postgres.mnnkthouavmpcycsvpog:YOUR_PASSWORD@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres?pgbouncer=true

DIRECT_DATABASE_URL=postgresql://postgres.mnnkthouavmpcycsvpog:YOUR_PASSWORD@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres

# CORS Settings (add your frontend URL)
CORS_ALLOWED_ORIGINS=https://printbox3d.com,https://www.printbox3d.com,http://localhost:3000

# Email Settings (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password
DEFAULT_FROM_EMAIL=noreply@printbox3d.com
```

#### Generate a Strong SECRET_KEY:
```python
# Run this in Python console
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### 3.3 Railway Will Auto-Deploy
Railway will automatically:
1. Install dependencies from `requirements.txt`
2. Run database migrations using `DIRECT_DATABASE_URL`
3. Collect static files
4. Start the server with Gunicorn

Monitor the deployment logs in Railway dashboard.

## Step 4: Post-Deployment Setup

### 4.1 Create Superuser
Use Railway CLI or go to Railway dashboard:

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Create superuser
railway run python manage.py createsuperuser
```

### 4.2 Verify Deployment
1. Visit `https://your-app-name.railway.app/admin/`
2. Login with superuser credentials
3. Test API endpoints: `https://your-app-name.railway.app/api/`

### 4.3 Add Sample Data (Optional)
```bash
railway run python manage.py populate_sample_data
```

## Step 5: Configure Custom Domain (Optional)

### 5.1 In Railway
1. Go to your service settings
2. Click "Generate Domain" or "Custom Domain"
3. Add your domain: `api.printbox3d.com`
4. Copy the CNAME record

### 5.2 In Your DNS Provider
Add CNAME record:
- **Type**: CNAME
- **Name**: api (or @)
- **Value**: `your-app-name.railway.app`

### 5.3 Update Environment Variables
```env
ALLOWED_HOSTS=api.printbox3d.com,printbox3d.com,your-app-name.railway.app
CORS_ALLOWED_ORIGINS=https://printbox3d.com,https://www.printbox3d.com
```

## Troubleshooting

### Database Connection Issues

**Problem**: `OperationalError: could not connect to server`
**Solution**: 
- Verify Supabase password is correct
- Check if your IP is whitelisted in Supabase (Settings → Database → Network)
- Ensure you're using the correct connection string

### Migration Errors

**Problem**: `Prepared statement already exists`
**Solution**:
- The code automatically uses `DIRECT_DATABASE_URL` for migrations
- This bypasses connection pooling (PgBouncer)
- Ensure `DIRECT_DATABASE_URL` uses port 5432 (not 6543)

### Static Files Not Loading

**Problem**: CSS/JS not loading in admin panel
**Solution**:
```bash
railway run python manage.py collectstatic --noinput
```

### CORS Errors

**Problem**: Frontend can't access API
**Solution**: Add frontend domain to `CORS_ALLOWED_ORIGINS` in Railway environment variables

## Database Architecture

### Connection Pooling vs Direct Connection

```
┌─────────────────────────────────────┐
│         Railway Application         │
│                                     │
│  ┌─────────────────────────────┐   │
│  │   Normal Operations         │   │
│  │   Uses: DATABASE_URL        │   │
│  │   Port: 6543 (PgBouncer)    │───┼──┐
│  └─────────────────────────────┘   │  │
│                                     │  │
│  ┌─────────────────────────────┐   │  │
│  │   Migrations                │   │  │
│  │   Uses: DIRECT_DATABASE_URL │   │  │
│  │   Port: 5432 (Direct)       │───┼──┤
│  └─────────────────────────────┘   │  │
└─────────────────────────────────────┘  │
                                         │
                                         ▼
                               ┌──────────────────┐
                               │  Supabase DB     │
                               │  PostgreSQL      │
                               │                  │
                               │  PgBouncer       │
                               │  (Port 6543)     │
                               │                  │
                               │  Direct Access   │
                               │  (Port 5432)     │
                               └──────────────────┘
```

**Why Two URLs?**
- **Connection Pooling (6543)**: Faster for normal operations, but doesn't support some migration operations
- **Direct Connection (5432)**: Required for migrations, supports all PostgreSQL features

## Monitoring

### Railway Dashboard
- View logs in real-time
- Monitor CPU/Memory usage
- Check deployment history

### Supabase Dashboard
- Monitor database size
- View active connections
- Check query performance
- Set up database backups

## Backup Strategy

### Automatic Backups (Supabase)
- Supabase automatically backs up your database
- Point-in-time recovery available on paid plans

### Manual Backup
```bash
# Export database
railway run python manage.py dumpdata > backup.json

# Import database
railway run python manage.py loaddata backup.json
```

## Scaling Considerations

### Database
- **Free Tier**: 500MB database, 2 direct connections
- **Pro Tier**: 8GB database, unlimited connections
- Connection pooling helps maximize connection usage

### Application
- Railway auto-scales based on traffic
- Consider upgrading plan for higher limits
- Monitor performance metrics

## Security Checklist

- [ ] `DEBUG=False` in production
- [ ] Strong `SECRET_KEY` (50+ characters)
- [ ] `ALLOWED_HOSTS` properly configured
- [ ] Database password is strong and secure
- [ ] CORS origins limited to your domains only
- [ ] Enable Supabase Network Restrictions (optional)
- [ ] Set up Railway environment variable protection
- [ ] Enable HTTPS (automatic with Railway)
- [ ] Regular database backups configured

## Cost Estimation

### Supabase
- **Free Tier**: $0/month (500MB database, 2 connections)
- **Pro Tier**: $25/month (8GB database, unlimited connections)

### Railway
- **Hobby Plan**: $5/month (first $5 free)
- **Actual Cost**: ~$5-10/month for small apps
- **Pro Plan**: $20/month for production apps

## Support Resources

- **Supabase Docs**: https://supabase.com/docs
- **Railway Docs**: https://docs.railway.app
- **Django Docs**: https://docs.djangoproject.com
- **Django + PostgreSQL**: https://docs.djangoproject.com/en/4.2/ref/databases/#postgresql-notes

---

**Last Updated**: November 2025
