#!/usr/bin/env python3
"""
Setup script for running DSA Study Planner locally
"""

import os
import subprocess
import sys

def install_requirements():
    """Install required packages"""
    packages = [
        'flask==3.0.0',
        'flask-sqlalchemy==3.1.1', 
        'flask-cors==4.0.0',
        'firebase-admin==6.4.0',
        'gunicorn==23.0.0',
        'psycopg2-binary==2.9.9',
        'sqlalchemy==2.0.25',
        'werkzeug==3.0.1',
        'email-validator==2.1.0'
    ]
    
    print("Installing required packages...")
    for package in packages:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
    print("✓ All packages installed successfully!")

def create_env_file():
    """Create example .env file"""
    env_content = """# Firebase Configuration
FIREBASE_API_KEY=your_firebase_api_key_here
FIREBASE_PROJECT_ID=your_firebase_project_id_here
FIREBASE_APP_ID=your_firebase_app_id_here
FIREBASE_SERVICE_ACCOUNT_KEY={"type":"service_account","project_id":"your-project"}

# App Configuration
SESSION_SECRET=your-secret-key-here
DATABASE_URL=sqlite:///local_dsa_study_plan.db

# Optional: For production PostgreSQL
# DATABASE_URL=postgresql://username:password@localhost:5432/dsa_study_plan
"""
    
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✓ Created .env file template")
        print("⚠️  Please edit .env file with your Firebase credentials")
    else:
        print("✓ .env file already exists")

def run_app():
    """Run the Flask application"""
    print("\n🚀 Starting DSA Study Planner...")
    print("📍 Access your app at: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    
    # Set environment variables
    os.environ['FLASK_APP'] = 'main.py'
    os.environ['FLASK_DEBUG'] = '1'
    
    # Import and run the app
    from main import app
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    print("🔧 Setting up DSA Study Planner for local development...")
    
    try:
        install_requirements()
        create_env_file()
        
        print("\n📝 Next steps:")
        print("1. Edit .env file with your Firebase credentials")
        print("2. Add 'localhost' to Firebase authorized domains")
        print("3. Run: python setup_local.py")
        
        input("\nPress Enter when ready to start the server...")
        run_app()
        
    except KeyboardInterrupt:
        print("\n👋 Setup cancelled by user")
    except Exception as e:
        print(f"❌ Error during setup: {e}")
        print("Please check the LOCAL_SETUP.md file for manual instructions")