#!/usr/bin/env python3
"""
Railway deployment script for Django Blog Application
This file helps Railway detect this as a Python project
"""

import os
import sys

if __name__ == "__main__":
    # Add backend directory to Python path
    backend_path = os.path.join(os.path.dirname(__file__), 'backend')
    sys.path.insert(0, backend_path)
    
    # Set Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_backend.settings')
    
    # Import and run Django
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
