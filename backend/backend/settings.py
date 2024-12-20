from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-j()*tiy80$l*ew8p!c&zob4auaz*0ll$+$amew&wwm779^m)$3')    

# SECURITY WARNING: don't run with debug turned on in production!
WEBSITE_HOSTNAME = os.environ.get('WEBSITE_HOSTNAME', None) 

DEBUG = WEBSITE_HOSTNAME == None 

if DEBUG: 

    ALLOWED_HOSTS = [] 

else: 

    ALLOWED_HOSTS = [WEBSITE_HOSTNAME] 

    CSRF_TRUSTED_ORIGINS = [f'https://{WEBSITE_HOSTNAME}'] 



if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = "DENY"

ALLOWED_HOSTS = [os.environ.get('WEBSITE_HOSTNAME', '')]
ALLOWED_HOSTS = ['c3054602app-a6cqdfa2aha0akf6.northeurope-01.azurewebsites.net']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'reviews.apps.ReviewsConfig',
    'users.apps.UsersConfig',
    'crispy_forms',
    'crispy_bootstrap4',
    'products.apps.ProductsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'users.middleware.AutoLogoutMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': os.environ['AZURE_DB_NAME'],   
        'USER': os.environ['AZURE_DB_USER'],
        'PASSWORD': os.environ['AZURE_DB_PASSWORD'],
        'HOST': os.environ['AZURE_DB_HOST'],
        'PORT': '1433',  # Default port for Azure SQL
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',  # Ensure the correct driver is specified
            'extra_params': "TrustServerCertificate=yes"
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

#STATIC_URL = 'static/'

#STATICFILES_DIRS = [
#    BASE_DIR / "static",
#]

#STATIC_ROOT = BASE_DIR / "staticfiles"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap4'
CRISPY_TEMPLATE_PACK = 'bootstrap4'

#MEDIA_URL = '/media/'
#MEDIA_ROOT = BASE_DIR / 'media'

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Mailtrap settings
EMAIL_HOST = "smtp.mailtrap.io"
EMAIL_PORT = 2525
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']   
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
DEFAULT_FROM_EMAIL = os.environ['DEFAULT_FROM_EMAIL']

# Path to save email records
EMAIL_LOG_PATH = BASE_DIR / "emails"

# Set session timeout to 10 minutes (600 seconds)
SESSION_COOKIE_AGE = 600  # Time in seconds
AUTO_LOGOUT_TIME = 600

# Weather API Key
WEATHER_API_KEY = os.environ['WEATHER_API_KEY']   

# Azure Storage Account details
AZURE_SA_NAME = os.environ['AZURE_SA_NAME']
AZURE_SA_KEY = os.environ['AZURE_SA_KEY']

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.azure_storage.AzureStorage",
        "OPTIONS": {
            "account_name": AZURE_SA_NAME,
            "account_key": AZURE_SA_KEY,
            "azure_container": "media",
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.azure_storage.AzureStorage",
        "OPTIONS": {
            "account_name": AZURE_SA_NAME,
            "account_key": AZURE_SA_KEY,
            "azure_container": "static",
        },
    },
}

STATIC_URL = f'https://{AZURE_SA_NAME}.blob.core.windows.net/static/'
MEDIA_URL = f'https://{AZURE_SA_NAME}.blob.core.windows.net/media/'
