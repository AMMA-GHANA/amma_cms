# AMMA CMS - Asokore Mampong Municipal Assembly Content Management System

## Overview
Modern Django-based CMS for managing the AMMA website with Tailwind CSS frontend.

## Tech Stack
- **Backend**: Django 5.0.8, Python 3.13
- **Frontend**: Tailwind CSS, Alpine.js, HTMX
- **Database**: SQLite (dev), PostgreSQL (production)
- **Rich Text Editor**: CKEditor 5
- **Admin Theme**: django-admin-interface

## Project Structure
```
amma_cms/
├── config/               # Project settings
│   ├── settings/
│   │   ├── base.py      # Base settings
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
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
├── static/             # Static files (CSS, JS)
├── media/              # User uploads
└── requirements/       # Python dependencies
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
pip install -r requirements/development.txt
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
```

Visit: http://127.0.0.1:8000

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

### Production Settings
Set environment variable:
```bash
export DJANGO_SETTINGS_MODULE=config.settings.production
```

### Static Files
```bash
python manage.py collectstatic
```

### Database Migration
```bash
python manage.py migrate --settings=config.settings.production
```

## Development

### Running Tests
```bash
pytest
```

### Creating Migrations
```bash
python manage.py makemigrations
```

### Django Shell
```bash
python manage.py shell_plus  # With django-extensions
```

## License
Proprietary - Asokore Mampong Municipal Assembly

## Support
For issues and questions, contact the development team.
