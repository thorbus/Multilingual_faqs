# Multilingual FAQ System

A Django-based FAQ management system with multilingual support, WYSIWYG editor integration, and efficient caching.

## Features

- Multilingual FAQ management (English, Hindi, Bengali)
- WYSIWYG editor support using django-ckeditor
- Automatic translation using Google Translate API
- Caching for improved performance
- RESTful API with language selection
- Comprehensive Django Admin interface


## Installation

1. Clone the repository:
```bash
https://github.com/thorbus/BharatFD_Assignment.git
cd faq_multilingual
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Make and Run migrations:
```bash
python manage.py makemigrations 
python manage.py migrate
```
6. Run Server
```bash
python manage.py runserver
```



## API Usage

### List FAQs

```bash
GET /api/faqs/
```

### Get FAQ in specific language

```bash
GET /api/faqs/?lang=hi
```

### Create new FAQ

```bash
POST /api/faqs/
{
    "question": "What is Django?",
    "answer": "Django is a web framework."
}
```

## Running Tests

```bash
pytest
```
