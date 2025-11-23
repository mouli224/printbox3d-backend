# PrintBox3D Backend - Deployment Guide for Railway

## Prerequisites

- GitHub account
- Railway account (sign up at https://railway.app)
- Git installed on your computer

## Step 1: Prepare Your Code

1. Make sure all your code is committed to Git:

```bash
git init
git add .
git commit -m "Initial commit"
```

2. Create a GitHub repository and push your code:

```bash
git remote add origin https://github.com/yourusername/printbox-backend.git
git branch -M main
git push -u origin main
```

## Step 2: Set Up Railway Project

1. Go to https://railway.app and sign in with GitHub
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your `printbox-backend` repository
5. Railway will automatically detect the Django project

## Step 3: Add PostgreSQL Database

1. In your Railway project dashboard, click "New"
2. Select "Database" → "PostgreSQL"
3. Railway will automatically create a PostgreSQL database
4. The `DATABASE_URL` environment variable will be automatically set

## Step 4: Configure Environment Variables

In Railway dashboard, go to your project → Variables tab and add:

```
SECRET_KEY=your-secret-key-here-make-it-random-and-long
DEBUG=False
ALLOWED_HOSTS=*.railway.app,printbox3d.com,www.printbox3d.com
CORS_ALLOWED_ORIGINS=https://printbox3d.com,https://www.printbox3d.com,http://localhost:3000
```

**Generate a secure SECRET_KEY:**

```python
# Run this in Python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

## Step 5: Deploy

1. Railway will automatically deploy your app
2. Wait for the build to complete (check the deployment logs)
3. Once deployed, you'll get a URL like: `https://your-app.railway.app`

## Step 6: Run Database Migrations

After deployment, run migrations using Railway CLI:

1. Install Railway CLI:

```bash
npm i -g @railway/cli
```

2. Login to Railway:

```bash
railway login
```

3. Link your project:

```bash
railway link
```

4. Run migrations:

```bash
railway run python manage.py migrate
```

5. Create superuser:

```bash
railway run python manage.py createsuperuser
```

## Step 7: Test Your API

Visit your Railway URL:
- API: `https://your-app.railway.app/api/`
- Admin: `https://your-app.railway.app/admin/`

## Step 8: Configure Custom Domain (Optional)

1. In Railway dashboard, go to Settings
2. Under "Domains", click "Generate Domain" or add a custom domain
3. If using custom domain, add DNS records as instructed by Railway

## Step 9: Set Up Continuous Deployment

Railway automatically deploys when you push to your main branch:

```bash
git add .
git commit -m "Update something"
git push origin main
```

Railway will automatically:
1. Pull the latest code
2. Install dependencies
3. Run migrations
4. Collect static files
5. Deploy the new version

## Environment Variables Reference

Required variables for production:

```env
# Required
SECRET_KEY=<generate-secure-random-key>
DEBUG=False
ALLOWED_HOSTS=*.railway.app,your-domain.com
DATABASE_URL=<automatically-set-by-railway>

# CORS
CORS_ALLOWED_ORIGINS=https://your-frontend.com,http://localhost:3000

# Optional: Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@printbox3d.com
```

## Troubleshooting

### Build Fails

Check Railway deployment logs for errors:
- Missing dependencies in `requirements.txt`
- Python version mismatch
- Syntax errors

### Database Connection Issues

- Verify `DATABASE_URL` is set automatically by Railway
- Check if PostgreSQL addon is running
- Run migrations again

### Static Files Not Loading

```bash
railway run python manage.py collectstatic --noinput
```

### Application Errors

1. Check Railway logs:
   - Go to your project → Deployments
   - Click on latest deployment
   - View logs

2. Enable debug temporarily:
   - Set `DEBUG=True` in Railway variables
   - Check detailed error messages
   - Remember to set back to `DEBUG=False`

### CORS Errors

Make sure `CORS_ALLOWED_ORIGINS` includes your frontend URL:

```env
CORS_ALLOWED_ORIGINS=https://printbox3d.com,https://www.printbox3d.com
```

## Managing Your Deployment

### View Logs

```bash
railway logs
```

### Run Commands

```bash
railway run python manage.py <command>
```

### Common Commands

```bash
# Create superuser
railway run python manage.py createsuperuser

# Run migrations
railway run python manage.py migrate

# Collect static files
railway run python manage.py collectstatic --noinput

# Access Django shell
railway run python manage.py shell
```

## Production Checklist

- [ ] `DEBUG=False` in production
- [ ] Strong `SECRET_KEY` set
- [ ] `ALLOWED_HOSTS` configured correctly
- [ ] Database migrations run
- [ ] Superuser created
- [ ] Static files collected
- [ ] CORS origins configured
- [ ] SSL/HTTPS enabled (automatic with Railway)
- [ ] Environment variables secured
- [ ] Backup strategy in place

## Scaling

Railway makes it easy to scale:

1. Go to your project settings
2. Adjust resources as needed
3. Railway will automatically handle load balancing

## Backups

### Database Backups

1. In Railway dashboard, go to PostgreSQL service
2. Click on "Backups"
3. Configure automatic backups

Or manually backup:

```bash
railway run pg_dump $DATABASE_URL > backup.sql
```

## Monitoring

- Check Railway dashboard for metrics
- Set up alerts in Railway settings
- Monitor logs regularly

## Cost Estimation

Railway pricing:
- Free tier: Limited resources, good for testing
- Pro tier: $5/month base + usage
- Database: Approximately $5-10/month

## Support

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- GitHub Issues: Create issues in your repo

---

**Your PrintBox3D backend is now live! 🚀**
