"""
Configuration settings for PDF Processor
"""

from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# PDF Processing settings
MAX_PDF_SIZE_MB = int(os.getenv("MAX_PDF_SIZE_MB", 100))
SUPPORTED_FORMATS = [".pdf"]

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = LOGS_DIR / "pdf_processor.log"
