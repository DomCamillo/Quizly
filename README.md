# Quizly - AI-Powered Quiz Generator

Quizly is a Django REST API application that automatically generates quizzes from YouTube videos. The application uses AI services (Whisper for transcription and Google Gemini for question generation) to create interactive learning materials.

## Technology Stack

**Backend Framework**
- Django 5.x
- Django REST Framework
- Simple JWT (Cookie-based authentication)

**AI & Video Processing**
- OpenAI Whisper (audio transcription)
- Google Gemini API (quiz generation)
- yt-dlp (YouTube video download)
- FFmpeg (audio/video processing)

**Database**
- SQLite (development)
- PostgreSQL (recommended for production)

## Prerequisites

- Python 3.10 or higher
- FFmpeg (must be installed globally)
- Git

## Installation

### 1. Install FFmpeg

FFmpeg is required for audio extraction from YouTube videos.

**macOS**
```bash
brew install ffmpeg
ffmpeg -version
```

**Windows**
```powershell
# Using Chocolatey or winget
 winget install ffmpeg
 choco install ffmpeg

# Or download manually from: https://www.gyan.dev/ffmpeg/builds/
# Extract to C:\ffmpeg and add C:\ffmpeg\bin to PATH
```

**Linux (Ubuntu/Debian)**
```bash
sudo apt update
sudo apt install ffmpeg
ffmpeg -version
```

### 2. Clone Repository

```bash
git clone https://github.com/yourusername/quizly.git
cd quizly
```

### 3. Create Virtual Environment

```bash
# Create virtual environment
python -m venv env

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate

# Windows:
env\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Configuration of Django Settings

**Add the following to `settings.py`:**

### 1. Installed Apps
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',


    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',


    'authentication',
    'quizzes',
    ...
]
```

### 2. Middleware
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

### 3. REST Framework Configuration
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

### 4. JWT Settings
```python
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_COOKIE': 'access_token',
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

### 5. CORS Configuration
```python
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', 'http://localhost:5000').split(',')
CORS_ALLOW_CREDENTIALS = True
```

### 6. Load Environment Variables
```python
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
```

### 1. Environment Variables

Create a `.env` file in the project root:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# API Keys
GOOGLE_API_KEY=your-google-gemini-api-key

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

**Generate Django Secret Key if needed:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 2. Get Google Gemini API Key

1. Visit: https://ai.google.dev/
2. solutions -> Gemini API -> create new API key
3. Add the key to your `.env` file

## Database Setup if needed

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

## Running the Application

```bash
# Start development server
python manage.py runserver

# Server runs on: http://127.0.0.1:8000
```

Access Django Admin at: http://127.0.0.1:8000/admin

## API Endpoints

### Authentication

**Register**
```http
POST /api/register/
Content-Type: application/json

{
  "username": "testuser",
  "email": "test@example.com",
  "password": "SecurePass123!",
  "confirmed_password": "SecurePass123!"
}
```

**Login**
```http
POST /api/login/
Content-Type: application/json

{
  "username": "testuser",
  "password": "SecurePass123!"
}
```

**Logout**
```http
POST /api/logout/
Authorization: Cookies (access_token)
```

**Refresh Token**
```http
POST /api/token/refresh/
Cookies: refresh_token
```

### Quiz Management

**Create Quiz from YouTube Video**
```http
POST /api/createQuiz/
Authorization: Cookies (access_token)
Content-Type: application/json

{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

**Get All Quizzes**
```http
GET /api/quizzes/
Authorization: Cookies (access_token)
```

**Get Single Quiz**
```http
GET /api/quizzes/{id}/
Authorization: Cookies (access_token)
```

**Update Quiz**
```http
PATCH /api/quizzes/{id}/
Authorization: Cookies (access_token)
Content-Type: application/json

{
  "title": "New Title",
  "description": "New Description"
}
```

**Delete Quiz**
```http
DELETE /api/quizzes/{id}/
Authorization: Cookies (access_token)
```

## Project Structure

```
quizly/
├── core/              # Main project settings
├── authentication/      # User authentication app
├── quizzes/               # Quiz management app
├── video_processing/      # Handles Quiz generation and Transcript
├── venv/               # Virtual environment
├── .env                # Environment variables
├── manage.py
├── requirements.txt
└── db.sqlite3
```

## License

This project is licensed under the MIT License.