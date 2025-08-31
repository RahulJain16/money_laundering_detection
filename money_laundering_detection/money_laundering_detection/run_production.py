"""
Production server runner for Money Laundering Detection System
Uses Waitress - a production WSGI server for Windows
"""
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set production environment
os.environ['FLASK_ENV'] = 'production'

try:
    from waitress import serve
    from app import app
    
    print("🚀 Starting Production Server...")
    print("🏛️  Money Laundering Detection System")
    print("🔒 Production Mode - Secure & Scalable")
    print("=" * 50)
    
    # Production server configuration
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    threads = int(os.environ.get('THREADS', 4))
    
    print(f"📍 Server: {host}:{port}")
    print(f"🧵 Threads: {threads}")
    print(f"🌐 Access: http://localhost:{port}")
    print("=" * 50)
    print("Press Ctrl+C to stop the server")
    
    # Start production server
    serve(app, host=host, port=port, threads=threads)
    
except ImportError:
    print("❌ Waitress not installed. Installing...")
    os.system("pip install waitress")
    print("✅ Please run this script again.")
    
except KeyboardInterrupt:
    print("\n🛑 Server stopped by user")
    
except Exception as e:
    print(f"❌ Error starting server: {e}")
    print("🔧 Falling back to development server...")
    from app import app
    app.run(host='0.0.0.0', port=5000, debug=False)
