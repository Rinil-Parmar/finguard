# FinGuard

FinGuard is a Django-based personal finance management web app for tracking transactions, budgets, savings goals, receipt uploads, user history, and rule-based fraud alerts.

## Features

- User registration, login, logout, and password reset
- CAD income and expense tracking
- Receipt uploads for PDF, JPG, JPEG, and PNG files
- Transaction search and filters
- Monthly budget management
- Savings goals with progress tracking
- Rule-based fraud alerts
- Session, cookie, and user activity history tracking
- Responsive Tailwind CSS interface

## Local Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
npm install
python manage.py migrate
npm run build:css
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Useful Commands

```bash
python manage.py createsuperuser
python manage.py check
python manage.py test
npm run build:css
```

## Environment Variables

Copy `.env.example` values into your deployment platform:

```text
DEBUG=False
SECRET_KEY=secure-production-secret
ALLOWED_HOSTS=your-domain.onrender.com
CSRF_TRUSTED_ORIGINS=https://your-domain.onrender.com
DATABASE_URL=postgres-connection-url
```

## Deployment

This project includes `render.yaml` and `build.sh` for Render deployment.

Render will:

- install Python dependencies
- install Node dependencies
- build Tailwind CSS
- collect static files
- run migrations
- start Django with Gunicorn

## CI

GitHub Actions runs on pushes and pull requests to `main`:

- install dependencies
- build Tailwind CSS
- run migrations
- run Django checks
- run tests
