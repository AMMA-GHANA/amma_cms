# AMMA CMS - Asokore Mampong Municipal Assembly Content Management System

## Overview
Modern Django-based CMS for managing the AMMA website with Tailwind CSS frontend.

## Tech Stack
- **Backend**: Django 5.0.8, Python 3.13
- **Frontend**: Tailwind CSS, Alpine.js
- **Database**: SQLite (flexible via DATABASE_URL for MySQL/PostgreSQL)
- **Rich Text Editor**: CKEditor 5
- **Admin Theme**: django-admin-interface

## Project Structure
```
amma_cms/
├── config/               # Project settings
│   ├── settings.py      # Django settings (consolidated)
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/                # Django applications
│   ├── core/           # Homepage & site settings
│   ├── news/           # News management
│   ├── projects/       # Projects management
│   ├── staff/          # Staff/Leadership
│   ├── services/       # Services
│   ├── documents/      # Downloads
│   ├── gallery/        # Photo gallery
│   └── contact/        # Contact forms
├── templates/          # HTML templates
├── theme/              # Tailwind CSS app
│   └── static_src/     # Tailwind source files
├── static/             # Static files (CSS, JS)
├── media/              # User uploads
├── requirements.txt    # Python dependencies
├── Makefile            # Development workflow commands
└── passenger_wsgi.py   # cPanel deployment
```

## Setup Instructions

### 1. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
# or using Makefile
make install
```

### 3. Environment Variables
Copy `.env.example` to `.env` and update values:
```bash
cp .env.example .env
```

### 4. Run Migrations
```bash
python manage.py migrate
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver
# or using Makefile
make run
```

Visit: http://127.0.0.1:8000

## Makefile Commands

The project includes a Makefile for streamlined development workflow:

```bash
make install          # Install Python dependencies
make migrate          # Create and run database migrations
make run              # Start Django development server
make shell            # Open Django shell
make test             # Run tests
make clean            # Remove Python cache files
make collectstatic    # Collect static files for production
make tailwind-watch   # Watch and compile Tailwind CSS (development)
make tailwind-build   # Build Tailwind CSS for production
make superuser        # Create Django superuser
make backup           # Backup SQLite database to backups/ directory
```

## Features

### Core Module
- Site-wide settings management
- Hero carousel for homepage
- Statistics cards
- About section management

### News Module
- Create/Edit/Delete news articles
- Rich text editor
- Featured news
- Categories and filtering
- View counter

### Projects Module
- Project management with multiple images
- Category-based filtering
- Status tracking (Planned/Ongoing/Completed)
- Impact metrics

### Staff Module
- Staff member profiles
- Leadership section
- Department organization
- Photo management

### Additional Modules
- Services management
- Document downloads with tracking
- Photo gallery with categories
- Contact form management

## Admin Panel
Access: http://127.0.0.1:8000/admin

Features:
- Modern, customizable interface
- Rich text editing
- Image upload and management
- Bulk actions
- Search and filtering

## Deployment

For detailed deployment instructions, see [CPANEL_DEPLOYMENT.md](CPANEL_DEPLOYMENT.md).

### Static Files
```bash
python manage.py collectstatic
# or
make collectstatic
```

### Database Migration
```bash
python manage.py migrate
# or
make migrate
```

### Environment Configuration
Ensure your `.env` file is properly configured for production:
- Set `DEBUG=False`
- Generate a unique `SECRET_KEY`
- Configure `ALLOWED_HOSTS` with your domain(s)
- Set up email settings for contact form functionality
- Enable `SESSION_COOKIE_SECURE=True` and `CSRF_COOKIE_SECURE=True` if using HTTPS

## Development

### Running Tests
```bash
python manage.py test
# or
make test
```

### Creating Migrations
```bash
python manage.py makemigrations
# or (includes migrate)
make migrate
```

### Django Shell
```bash
python manage.py shell
# or
make shell
```

## Database Configuration

The project uses **SQLite by default** for both development and production, which is suitable for small to medium-sized sites. You can configure alternative database backends via the `DATABASE_URL` environment variable in your `.env` file:

**SQLite (default):**
```env
DATABASE_URL=sqlite:///db.sqlite3
```

**MySQL:**
```env
DATABASE_URL=mysql://username:password@localhost/database_name
```

**PostgreSQL:**
```env
DATABASE_URL=postgres://username:password@localhost/database_name
```

The settings use `django-environ` to parse the `DATABASE_URL`, making it easy to switch between database backends without code changes.

## License
Proprietary - Asokore Mampong Municipal Assembly

## Support
For issues and questions, contact the development team.
