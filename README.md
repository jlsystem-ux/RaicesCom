# RaicesCom

A Django web application for Raíces Compartidas, supporting refugees and cultural integration.

## Features
- Multilingual support (English and Spanish) using Django i18n
- Event management and listing
- Google Cloud Translation integration (English-Spanish, Spanish-English)
- User authentication (login/logout)
- Responsive design with Bootstrap

## Setup

### 1. Clone the repository
```
git clone https://github.com/jlsystem-ux/RaicesCom.git
cd RaicesCom
```

### 2. Create and activate a virtual environment
```
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate
# Or, if you get a policy error:
cmd /c venv\Scripts\activate.bat
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the project root (see `.env.example` or below):
```
DEBUG=True
SECRET_KEY=your-django-secret-key
DB_NAME=raicesCompartidas_db
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Database migrations
```
python manage.py migrate
```

### 6. Compile translations (Windows)
Make sure GNU gettext is installed and `msgfmt` is in your PATH.
```
python manage.py compilemessages
```

### 7. Run the development server
```
python manage.py runserver
```

Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## Translation
- Use the language selector in the footer to switch between English and Spanish.
- To add or update translations:
  1. Mark text in templates with `{% trans %}` or `{% blocktrans %}`.
  2. Run `python manage.py makemessages -l es` and/or `-l en`.
  3. Edit `.po` files in `locale/`.
  4. Run `python manage.py compilemessages`.

## Deployment
- Set `DEBUG=False` and configure allowed hosts and secure settings in `.env` for production.
- Use a production server (e.g., Gunicorn) and a reverse proxy (e.g., Nginx).

## NHS Info Card
- In the footer, click "NHS" under "Recursos de Emergencia" to view an information card with emergency and non-emergency phone numbers for the UK National Health Service. Click "Cerrar" to close the card.

## License
MIT
