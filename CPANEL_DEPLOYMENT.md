# cPanel Deployment Guide for AMMA CMS

This guide provides step-by-step instructions for deploying the AMMA CMS Django application on cPanel hosting with SQLite database.

## Prerequisites

- cPanel hosting account with Python support
- SSH access (recommended but not required)
- Domain name configured in cPanel

## Step 1: Prepare Your Local Project

1. **Generate a production secret key:**
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

2. **Test locally with production settings:**
```bash
# Copy .env.example to .env and update values
cp .env.example .env

# Edit .env with your production values
# Set DEBUG=False
# Set your domain in ALLOWED_HOSTS
# Add the generated SECRET_KEY
```

3. **Collect static files:**
```bash
python manage.py collectstatic --noinput
```

## Step 2: Upload Files to cPanel

### Option A: Using Git (Recommended)

1. **Login to cPanel and open Terminal**

2. **Clone your repository:**
```bash
cd ~/
git clone https://github.com/yourusername/amma_cms.git
```

### Option B: Using File Manager or FTP

1. Upload all project files to your home directory or desired location
2. Ensure the following structure:
```
/home/username/amma_cms/
├── apps/
├── config/
├── media/
├── static/
├── staticfiles/
├── templates/
├── theme/
├── .env
├── .htaccess
├── db.sqlite3
├── manage.py
├── passenger_wsgi.py
└── requirements.txt
```

## Step 3: Set Up Python Environment in cPanel

1. **Navigate to cPanel → Setup Python App**

2. **Create New Python Application:**
   - Python version: 3.9 or higher
   - Application root: `/home/username/amma_cms`
   - Application URL: Your domain or subdomain
   - Application startup file: `passenger_wsgi.py`
   - Application Entry point: `application`

3. **Note the virtual environment path** (something like):
   ```
   /home/username/virtualenv/amma_cms/3.9
   ```

4. **Update passenger_wsgi.py** with the correct path:
   - Edit line 9: `INTERP = os.path.expanduser("~/virtualenv/amma_cms/3.9/bin/python3")`
   - Replace with your actual virtual environment path

## Step 4: Install Python Dependencies

1. **Enter the virtual environment:**
```bash
source /home/username/virtualenv/amma_cms/3.9/bin/activate
cd ~/amma_cms
```

2. **Install requirements:**
```bash
pip install -r requirements.txt
```

## Step 5: Configure Environment Variables

1. **Create/Edit .env file in project root:**
```bash
nano ~/amma_cms/.env
```

2. **Set production values:**
```env
DEBUG=False
SECRET_KEY=your-generated-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Email settings
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=mail.yourdomain.com
EMAIL_PORT=587
EMAIL_HOST_USER=noreply@yourdomain.com
EMAIL_HOST_PASSWORD=your-email-password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=noreply@amma.gov.gh

# Security (if using HTTPS)
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

## Step 6: Set Up Database

1. **Run migrations:**
```bash
source /home/username/virtualenv/amma_cms/3.9/bin/activate
cd ~/amma_cms
python manage.py migrate
```

2. **Create superuser:**
```bash
python manage.py createsuperuser
```

3. **Set proper permissions for SQLite database:**
```bash
chmod 664 db.sqlite3
chmod 775 ~/amma_cms
```

## Step 7: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

This will collect all static files to the `staticfiles/` directory.

## Step 8: Configure .htaccess

1. **Edit .htaccess in project root** and update paths:
```apache
PassengerAppRoot /home/username/amma_cms
PassengerPython /home/username/virtualenv/amma_cms/3.9/bin/python3
```

2. **Copy .htaccess to public_html** (if your app is in the main domain):
```bash
cp ~/amma_cms/.htaccess ~/public_html/.htaccess
```

## Step 9: Set Up Static and Media File Serving

### Option A: Serve from Application Directory

Create symbolic links in your public_html:
```bash
ln -s ~/amma_cms/staticfiles ~/public_html/static
ln -s ~/amma_cms/media ~/public_html/media
```

### Option B: Copy Static Files to public_html

```bash
cp -r ~/amma_cms/staticfiles ~/public_html/static
cp -r ~/amma_cms/media ~/public_html/media
```

**Note:** If you use Option B, you'll need to recopy static files after running `collectstatic`.

## Step 10: Restart the Application

After making changes, restart your Python application:

### Method 1: Using cPanel
- Go to Setup Python App
- Click "Restart" button

### Method 2: Using SSH
```bash
mkdir -p ~/amma_cms/tmp
touch ~/amma_cms/tmp/restart.txt
```

## Troubleshooting

### Static Files Not Loading

1. **Check .htaccess rewrite rules** are allowing static files:
```apache
RewriteCond %{REQUEST_URI} ^/static/ [NC]
RewriteRule ^(.*)$ - [L]
```

2. **Verify symbolic links:**
```bash
ls -la ~/public_html/static
ls -la ~/public_html/media
```

3. **Check file permissions:**
```bash
chmod -R 755 ~/amma_cms/staticfiles
chmod -R 755 ~/amma_cms/media
```

### Application Not Starting

1. **Check error logs:**
```bash
tail -f ~/logs/error_log
```

2. **Verify Python path in passenger_wsgi.py** matches your virtual environment

3. **Check .env file** is in the correct location with correct values

4. **Verify ALLOWED_HOSTS** includes your domain

### Database Errors

1. **Check SQLite file permissions:**
```bash
chmod 664 ~/amma_cms/db.sqlite3
chmod 775 ~/amma_cms
```

2. **Verify database path** in .env is correct

3. **Run migrations again:**
```bash
python manage.py migrate
```

### 500 Internal Server Error

1. **Enable debug temporarily** (don't forget to disable after):
   - Set `DEBUG=True` in .env
   - Restart application
   - Check the detailed error page
   - Set `DEBUG=False` again

2. **Check Python errors:**
```bash
tail -f ~/logs/error_log
```

## Updating the Application

When you need to update your application:

1. **Pull latest changes** (if using Git):
```bash
cd ~/amma_cms
git pull origin main
```

2. **Activate virtual environment:**
```bash
source /home/username/virtualenv/amma_cms/3.9/bin/activate
```

3. **Install any new dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run migrations:**
```bash
python manage.py migrate
```

5. **Collect static files:**
```bash
python manage.py collectstatic --noinput
```

6. **Restart application:**
```bash
touch ~/amma_cms/tmp/restart.txt
```

## Security Checklist

Before going live, ensure:

- [ ] `DEBUG=False` in .env
- [ ] Strong `SECRET_KEY` generated and set
- [ ] `ALLOWED_HOSTS` contains only your domain(s)
- [ ] `.env` file permissions are secure (chmod 600)
- [ ] Database file permissions are correct (chmod 664)
- [ ] SSL certificate is installed (HTTPS enabled)
- [ ] `SESSION_COOKIE_SECURE=True` if using HTTPS
- [ ] `CSRF_COOKIE_SECURE=True` if using HTTPS
- [ ] Admin URL is secured (consider changing admin path)

## Backup Strategy

### Database Backup
```bash
# Create backup
cp ~/amma_cms/db.sqlite3 ~/backups/db.sqlite3.$(date +%Y%m%d)

# Automate with cron job (in cPanel Cron Jobs)
0 2 * * * cp ~/amma_cms/db.sqlite3 ~/backups/db.sqlite3.$(date +\%Y\%m\%d)
```

### Media Files Backup
```bash
tar -czf ~/backups/media-$(date +%Y%m%d).tar.gz ~/amma_cms/media/
```

## Performance Tips

1. **Enable caching** - Add caching configuration in settings.py
2. **Optimize images** - Use image optimization tools for uploaded media
3. **Use CDN** - Consider CloudFlare for static files
4. **Monitor logs** - Regularly check error logs for issues

## Migrating to MySQL (Future)

When ready to move from SQLite to MySQL:

1. **Create MySQL database** in cPanel
2. **Update DATABASE_URL** in .env:
   ```
   DATABASE_URL=mysql://username:password@localhost/database_name
   ```
3. **Install MySQL driver:**
   ```bash
   pip install mysqlclient
   ```
4. **Migrate data** using Django dumpdata/loaddata or third-party tools
5. **Run migrations** and restart application

## Support

For issues specific to:
- **Django**: https://docs.djangoproject.com/
- **cPanel Python Apps**: Contact your hosting provider
- **AMMA CMS**: Check project documentation or contact development team
