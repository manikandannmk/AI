"""
Configuration file for Flask application
"""

import os
from pathlib import Path

# Base configuration
BASE_DIR = Path(__file__).resolve().parent

# Flask Configuration
DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
TESTING = os.getenv('FLASK_TESTING', 'False') == 'True'
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Upload Configuration
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 MB
UPLOAD_FOLDER = BASE_DIR / 'uploads'
OUTPUT_FOLDER = BASE_DIR / 'output'
ALLOWED_EXTENSIONS = {'pdf'}

# Create directories if they don't exist
UPLOAD_FOLDER.mkdir(exist_ok=True)
OUTPUT_FOLDER.mkdir(exist_ok=True)
Path('logs').mkdir(exist_ok=True)

# Server Configuration
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5000))

# Logging Configuration
LOG_FILE = BASE_DIR / 'logs' / 'app.log'
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# CORS Configuration
CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')

# PDF Processing Configuration
MAX_PDF_SIZE_MB = int(os.getenv('MAX_PDF_SIZE_MB', '100'))
EXTRACT_TEXT_MAX_LENGTH = int(os.getenv('EXTRACT_TEXT_MAX_LENGTH', '10000'))
TIMEOUT_SECONDS = int(os.getenv('TIMEOUT_SECONDS', '300'))

# Security Configuration
SECURE_FILENAME_ENABLED = True
INPUT_VALIDATION_ENABLED = True
