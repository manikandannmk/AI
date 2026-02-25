#!/usr/bin/env python
"""
Quick start script for running the PDF Processor web application
"""

import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Check if all requirements are installed"""
    print("Checking requirements...")
    try:
        import flask
        import pdf_processor
        print("✓ All requirements satisfied")
        return True
    except ImportError as e:
        print(f"✗ Missing requirement: {e}")
        print("\nInstalling requirements...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        return True

def create_directories():
    """Create necessary directories"""
    dirs = ['uploads', 'output', 'logs']
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
    print("✓ Directories ready")

def print_header():
    """Print application header"""
    print("\n" + "="*60)
    print("  PDF PROCESSOR - Web Interface")
    print("="*60 + "\n")

def print_instructions():
    """Print usage instructions"""
    print("\n📖 QUICK START GUIDE:\n")
    print("1. The application is now running on: http://localhost:5000")
    print("2. Open http://localhost:5000 in your web browser")
    print("3. Upload PDF files using drag-and-drop or file browser")
    print("4. Select processing options (extract text, metadata, etc.)")
    print("5. Click 'Process Files' to start processing")
    print("6. View and download results\n")
    
    print("💡 FEATURES:")
    print("   • Drag-and-drop file upload")
    print("   • Extract text from PDFs")
    print("   • Extract metadata and information")
    print("   • Extract tables and structures")
    print("   • Extract embedded images")
    print("   • Merge, split, and rotate PDFs\n")
    
    print("📝 KEYBOARD SHORTCUTS:")
    print("   • Ctrl+C: Stop the application")
    print("   • Press Ctrl+Z then Enter (if stuck)\n")

def main():
    """Main entry point"""
    print_header()
    
    # Check requirements
    if not check_requirements():
        print("Failed to install requirements")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Print instructions
    print_instructions()
    
    print("="*60)
    print("Starting Flask application...")
    print("="*60 + "\n")
    
    try:
        # Import and run Flask app
        from app_advanced import app
        
        print("✓ Application started successfully!")
        print("✓ Press Ctrl+C to stop the application\n")
        
        # Run the Flask application
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=True
        )
    except KeyboardInterrupt:
        print("\n\n✓ Application stopped gracefully")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error starting application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
