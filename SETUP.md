# Setup Instructions

## Quick Start

1. **Install Required Packages**
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install Django==5.2.7
pip install djangorestframework==3.15.2
pip install djangorestframework-simplejwt==5.3.1
pip install django-cors-headers==4.6.0
pip install Pillow==11.0.0
```

2. **Run Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

3. **Create Superuser (Optional)**
```bash
python manage.py createsuperuser
```

4. **Run Development Server**
```bash
python manage.py runserver
```

5. **Access the API**
- API Base URL: http://localhost:8000/api/
- Admin Panel: http://localhost:8000/admin/

## Testing the API

Use the examples in README.md to test the endpoints with cURL or Postman.

## Project Structure

```
masklens_backend/
├── backend/                    # Main app
│   ├── migrations/            # Database migrations
│   ├── models.py              # User, FacialAnalysis, WeeklySummary models
│   ├── serializers.py         # API serializers
│   ├── views.py               # API views
│   ├── urls.py                # App URLs
│   └── admin.py               # Admin configuration
├── masklens_backend/          # Project settings
│   ├── settings.py            # Django settings
│   ├── urls.py                # Main URL configuration
│   └── wsgi.py                # WSGI configuration
├── media/                     # Uploaded images (created automatically)
├── db.sqlite3                 # SQLite database
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
└── README.md                  # API documentation
```
