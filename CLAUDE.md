# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

RaicesCom is a Django web application for Raíces Compartidas, supporting refugees and cultural integration. It features multilingual support (English/Spanish), event management, Google Cloud Translation integration, and responsive design.

## Technology Stack

- **Backend**: Django 5.2.1 with Python
- **Database**: MySQL (production on PythonAnywhere), SQLite (development fallback)
- **Frontend**: HTML templates with Bootstrap, vanilla JavaScript
- **Static Files**: WhiteNoise with Django Compressor for CSS/JS minification
- **Translation**: Django i18n with Google Cloud Translation API
- **Deployment**: PythonAnywhere with Gunicorn

## Development Commands

### Environment Setup
```bash
# Create and activate virtual environment
python -m venv venv
# Windows PowerShell:
.\venv\Scripts\Activate
# Or if policy error:
cmd /c venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt
```

### Database Operations
```bash
# Apply migrations
python manage.py migrate

# Create new migrations after model changes
python manage.py makemigrations

# Create superuser
python manage.py createsuperuser
```

### Translation Management
```bash
# Extract translatable strings and create/update .po files
python manage.py makemessages -l es
python manage.py makemessages -l en

# Compile translation files (.po to .mo)
python manage.py compilemessages
```

### Development Server
```bash
# Run development server
python manage.py runserver

# Run with specific port
python manage.py runserver 8080
```

### Static Files
```bash
# Collect static files for production
python manage.py collectstatic

# Compress CSS/JS files
python manage.py compress
```

## Architecture Overview

### Core Application Structure
- **Core App** (`core/`): Main application logic containing models, views, and business logic
- **Project Settings** (`raicescom/`): Django project configuration and URL routing
- **Templates** (`templates/`): HTML templates with base template inheritance
- **Static Files** (`static/`): CSS, JavaScript, and image assets

### Key Models
- **Event**: Multilingual event management with image upload and online/in-person support
- **Resource**: Categorized resources with multilingual content
- **Category**: Resource categorization system
- **UserProfile**: Extended user profiles with language preferences

### URL Structure
- Internationalized URLs with language prefixes (`/en/`, `/es/`)
- API endpoints for translation (`/api/translate/`)
- Admin interface at `/admin/`
- Authentication URLs under `/accounts/`

### Translation System
- Dual approach: Django i18n for interface + Google Cloud Translation API for dynamic content
- Model fields have separate English/Spanish versions (`title_en`, `title_es`)
- Template strings use `{% trans %}` and `{% blocktrans %}` tags

## Environment Configuration

Required environment variables in `.env`:
- `SECRET_KEY`: Django secret key
- `DEBUG`: Boolean for debug mode
- `DB_PASSWORD`: Database password for production MySQL

Google Cloud credentials should be placed in `secrets/google-credentials.json`.

## File Organization

- **Templates**: Located in `templates/` with app-specific subdirectories
- **Static Assets**: Organized in `static/css/`, `static/js/`, `static/img/`
- **Media Uploads**: User uploads go to `media/` directory
- **Database**: SQLite file `db.sqlite3` for development

## Key Features

### Multilingual Support
- Interface available in English and Spanish
- Language switching via footer selector
- Automatic locale detection and URL prefixing

### Event Management
- Create events with multilingual titles/descriptions
- Support for both online (with meeting links) and in-person events
- Image upload with validation and automatic cleanup
- Calendar integration ready

### Translation Integration
- Google Cloud Translation API for real-time translation
- CSRF-protected translation endpoint
- Error handling and logging for translation failures

## Production Notes

- MySQL database configured for PythonAnywhere hosting
- WhiteNoise handles static file serving
- Security headers and HTTPS enforcement in production
- Compressed and minified CSS/JS assets