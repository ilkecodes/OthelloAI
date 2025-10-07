import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from main import app

# Vercel handler
def handler(request, context):
    return app(request, context)
