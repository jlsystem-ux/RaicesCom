# RaicesCom Setup Troubleshooting Guide

This document contains solutions to common issues encountered during RaicesCom development setup.

## Environment Information
- **Python Version**: 3.13.7
- **Operating System**: Windows 10/11
- **Database**: PostgreSQL (local development)

## Common Issues and Solutions

### 1. Django Installation Issues

**Problem**: `ModuleNotFoundError: No module named 'django'`

**Solution**:
```cmd
# Ensure virtual environment is activated
venv\Scripts\activate.bat

# Install Django specifically
pip install Django==5.2.1
```

### 2. Python-dotenv Missing

**Problem**: `ModuleNotFoundError: No module named 'dotenv'`

**Solution**:
```cmd
pip install python-dotenv==1.0.1
```

### 3. PostgreSQL Connection Issues (psycopg2)

**Problem**:
- `psycopg2-binary` compilation fails on Python 3.13
- Error: `unresolved external symbol _PyInterpreterState_Get`

**Solution**:
```cmd
# Use psycopg2 instead of psycopg2-binary
pip install psycopg2
```

### 4. Django-compressor Missing

**Problem**: `ModuleNotFoundError: No module named 'compressor'`

**Solution**:
```cmd
pip install django-compressor
```

### 5. UTF-8 Database Connection Error

**Problem**: `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xf3`

**Solutions**:

**Option A**: Update database password in settings.py
```python
# In raicescom/settings.py, line 118
'PASSWORD': 'root',  # Instead of get_env_value('DB_PASSWORD')
```

**Option B**: Create database with proper encoding
```cmd
createdb -U postgres -E UTF8 raicesCompartidas_db
```

**Option C**: Use simpler database name in .env
```
DB_NAME=raices_db
```

### 6. Network Connectivity Issues

**Problem**: `pip` timeouts when installing packages

**Solutions**:
```cmd
# Install essential packages individually
pip install Django==5.2.1
pip install python-dotenv==1.0.1
pip install psycopg2
pip install django-compressor
pip install Pillow
pip install whitenoise

# Or use alternative index
pip install -i https://pypi.org/simple/ package_name
```

## Step-by-Step Setup Process

### 1. Prerequisites
- Python 3.11+ installed
- PostgreSQL server running locally
- Git for cloning repository

### 2. Project Setup
```cmd
# Navigate to project directory
cd C:\Users\[USERNAME]\Documents\RaicesCom\RaicesCom-master\RaicesCom-master

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate.bat
```

### 3. Install Dependencies
```cmd
# Install core packages
pip install Django==5.2.1
pip install python-dotenv==1.0.1
pip install psycopg2
pip install django-compressor
pip install Pillow
pip install whitenoise

# Or try requirements.txt (may have network issues)
pip install -r requirements.txt
```

### 4. Database Configuration

**Check .env file**:
```
DEBUG=True
SECRET_KEY=django-insecure-s!u!*=0a&bj(pd!1v4v)v2(l--qk0424&yodw@e1ai2l-!ah(v
DB_NAME=raicesCompartidas_db
DB_USER=postgres
DB_PASSWORD=root
DB_HOST=localhost
DB_PORT=5432
```

**Create PostgreSQL database**:
```cmd
createdb -U postgres raicesCompartidas_db
```

### 5. Run Migrations
```cmd
python manage.py migrate
```

### 6. Create Superuser for Admin Access
```cmd
python manage.py createsuperuser
```
Follow the prompts to set username, email, and password.

### 7. Start Development Server
```cmd
python manage.py runserver
```

**Access application**:
- Main site: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/

## Alternative Solutions

### If PostgreSQL Issues Persist
Temporarily switch to SQLite by modifying `raicescom/settings.py`:

```python
# Replace PostgreSQL configuration with:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### If Virtual Environment Issues
```cmd
# Delete and recreate virtual environment
rmdir /s venv
python -m venv venv
venv\Scripts\activate.bat
```

## Verification Commands

**Check installations**:
```cmd
python --version
pip --version
python -c "import django; print(django.get_version())"
psql --version
```

**Test database connection**:
```cmd
python manage.py dbshell
```

## Common Commands Reference

```cmd
# Activate virtual environment
venv\Scripts\activate.bat

# Install single package
pip install package_name

# Run migrations
python manage.py migrate

# Create new migrations
python manage.py makemigrations

# Start development server
python manage.py runserver

# Create superuser
python manage.py createsuperuser

# Create sample data
python manage.py create_sample_events
```

## Files Modified During Setup

1. **raicescom/settings.py**: Changed database password from environment variable to hardcoded 'root'
2. **.env**: Contains database configuration variables

## Notes
- This setup uses PostgreSQL for development (as intended by the project)
- The hardcoded password 'root' in settings.py is a workaround for UTF-8 encoding issues
- All migrations completed successfully with this configuration
- The application starts successfully on http://127.0.0.1:8000/

## Support
If issues persist, check:
1. PostgreSQL service is running
2. Database exists and is accessible
3. Virtual environment is activated
4. All required packages are installed
5. Environment variables are properly set