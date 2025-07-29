# DSA Study Planner - Local Setup Guide

## Prerequisites
- Python 3.11 or higher
- pip (Python package manager)

## Step 1: Download the Code
1. Download all files from this Replit to your local machine
2. Create a new folder called `dsa_study_planner`
3. Copy all files to this folder

## Step 2: Install Dependencies
Open terminal/command prompt in your project folder and run:

```bash
pip install flask flask-sqlalchemy flask-cors firebase-admin gunicorn
```

## Step 3: Set Environment Variables
Create a `.env` file in your project root with:

```
FIREBASE_API_KEY=AIzaSyCM4RqLyKdm8pcQwqRuEVlieP3epYKyPLI
FIREBASE_PROJECT_ID=prepmate-2dfa5
FIREBASE_APP_ID=1:1001637355899:web:21b94953cd1c820d211dde
FIREBASE_SERVICE_ACCOUNT_KEY={"type":"service_account",...your full JSON key...}
SESSION_SECRET=your-secret-key-here
DATABASE_URL=sqlite:///local_dsa_study_plan.db
```

## Step 4: Update Firebase Authorized Domains
1. Go to Firebase Console (https://console.firebase.google.com/project/prepmate-2dfa5)
2. Authentication > Settings > Authorized domains
3. Add: `localhost`

## Step 5: Run the Application
```bash
python main.py
```

Your app will be available at: http://localhost:5000

## Alternative: Using Python's built-in server
If you prefer a simpler approach:

```bash
python -c "
import os
os.environ['FLASK_APP'] = 'main.py'
os.environ['FLASK_DEBUG'] = '1'
from main import app
app.run(host='0.0.0.0', port=5000, debug=True)
"
```

## Free Hosting Alternatives

### 1. Railway (Recommended Free Option)
- Sign up at railway.app
- Connect your GitHub repository
- Automatic deployments
- Free tier: 500 hours/month

### 2. Render
- Sign up at render.com
- Connect GitHub repo
- Free tier available
- Automatic SSL certificates

### 3. Replit (Current Platform)
- Keep using this Replit for free
- Share the URL with others
- Always available at your current Replit URL

### 4. GitHub Codespaces
- Run directly in GitHub's cloud environment
- Free tier: 60 hours/month

## Production Notes
- For production, use PostgreSQL instead of SQLite
- Set proper environment variables
- Use a production WSGI server like Gunicorn
- Add proper error logging and monitoring