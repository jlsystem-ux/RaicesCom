# RaicesCom - Raíces Compartidas

A Django web application for **Raíces Compartidas** (Shared Roots), supporting refugees and asylum seekers with cultural integration and community resources in the United Kingdom.

## 🌐 Live Website
**Production**: https://raicescompartidas.pythonanywhere.com

## ✨ Key Features

### Core Functionality
- **Multilingual Support**: Full English/Spanish interface with Django i18n
- **Event Management**: Community events, workshops, and cultural celebrations
- **Blog System**: News, community stories, guides, and updates
- **Resource Library**: Categorized support materials and guides
- **Contact System**: Staff profiles with contact information and social media
- **Testimonials**: Community success stories and experiences

### Advanced Features
- **Google Cloud Translation API**: Real-time content translation
- **Responsive Design**: Bootstrap-based mobile-friendly interface
- **SEO Optimized**: Structured data, sitemaps, and multilingual SEO
- **Media Management**: Image uploads with validation and optimization
- **Admin Dashboard**: Content management through Django admin
- **Security**: Production-ready security settings and HTTPS

## 🚀 Technology Stack

- **Backend**: Django 5.2.1 with Python 3.10
- **Database**: MySQL (Production on PythonAnywhere) / PostgreSQL (Development)
- **Frontend**: HTML templates with Bootstrap 5, Vanilla JavaScript
- **Static Files**: WhiteNoise with Django Compressor for CSS/JS optimization
- **Translation**: Django i18n + Google Cloud Translation API
- **Deployment**: PythonAnywhere with Gunicorn
- **Version Control**: Git with GitHub repository

## 🛠️ Local Development Setup

### 1. Clone the repository
```bash
git clone https://github.com/jlsystem-ux/RaicesCom.git
cd RaicesCom
```

### 2. Create and activate virtual environment
```bash
# Create virtual environment
python -m venv venv

# Windows PowerShell:
.\venv\Scripts\Activate

# Or if policy error:
cmd /c venv\Scripts\activate.bat

# macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the project root:
```env
DEBUG=True
SECRET_KEY=your-django-secret-key-here
PRODUCTION=false

# PostgreSQL (Development)
DB_NAME=raicescompartidas_db
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Database Setup
```bash
# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 6. Translation Setup
```bash
# Compile translation files
python manage.py compilemessages
```

### 7. Static Files
```bash
# Collect static files
python manage.py collectstatic
```

### 8. Run Development Server
```bash
python manage.py runserver
```
Visit: http://127.0.0.1:8000

## 🌍 Production Deployment (PythonAnywhere)

### Environment Variables
```env
DEBUG=False
SECRET_KEY=your-production-secret-key
PRODUCTION=true
DB_PASSWORD=your-mysql-password
```

### Database Configuration
- **Database**: `Raicescompartida$raicescompartidas_db`
- **Host**: `Raicescompartida.mysql.pythonanywhere-services.com`
- **User**: `Raicescompartida`

### Key Directories
- **Source Code**: `/home/Raicescompartidas/RaicesCom`
- **Static Files**: `/home/Raicescompartidas/RaicesCom/staticfiles/`
- **Media Files**: `/home/Raicescompartidas/RaicesCom/media/`
- **Virtual Environment**: `/home/Raicescompartidas/venv`

## 📚 Content Management

### Event Management
- Create online/in-person events
- Multilingual titles and descriptions
- Image uploads with automatic optimization
- Meeting link integration for online events

### Blog System
- Multiple post types: News, Community Stories, Guides, Updates
- Category organization with color coding
- Featured posts and SEO optimization
- Reading time estimation

### Staff Profiles
- Contact information with WhatsApp integration
- Social media links (Facebook, Twitter, LinkedIn)
- Professional photos and biographies
- Display settings for contact page

### Testimonials
- Community success stories
- Country of origin tracking
- Consent management
- Featured testimonials

## 🔧 Translation Management

### Adding New Translations
```bash
# Extract translatable strings
python manage.py makemessages -l es
python manage.py makemessages -l en

# Edit translation files in locale/ directory
# Compile translations
python manage.py compilemessages
```

### Google Cloud Translation
- Real-time translation API integration
- Automatic language detection
- Error handling and logging
- CSRF protection

## 🎯 Target Audience

**Primary Users:**
- Refugees and asylum seekers in the UK
- Spanish-speaking communities
- Support organizations and volunteers
- Legal advisors and social workers

**Key Resources:**
- NHS and healthcare guidance
- Legal process information
- Cultural integration support
- Community events and networking
- Mental health and wellbeing resources

## 📱 Features Overview

### Homepage Sections
- **Welcome Banner**: Mission and vision
- **About Us**: Organization information
- **Resources**: 6 key support categories:
  - Meditation & Mindfulness
  - Emotional Self-Care
  - Community Support
  - Educational Resources
  - Practical Support (NHS, housing, food banks)
  - Cultural Resources

### Emergency Resources
- NHS emergency contacts (999, 111)
- Crisis support information
- Direct links to healthcare services

## 🔒 Security Features

- HTTPS enforcement in production
- CSRF protection on all forms
- Secure session management
- Content Security Policy headers
- SQL injection protection
- File upload validation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For technical support or questions about deployment:
- Repository: https://github.com/jlsystem-ux/RaicesCom
- Live Website: https://raicescompartidas.pythonanywhere.com
- Admin Panel: https://raicescompartidas.pythonanywhere.com/admin

---

**Raíces Compartidas** - Supporting refugee communities through technology, resources, and human connection. 🌟