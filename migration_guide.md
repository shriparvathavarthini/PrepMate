# DSA Study Planner - Migration to Render.com

## Overview
This guide helps you migrate from Replit to Render.com with a free external database.

## Option 1: Render + Supabase (Recommended)

### Step 1: Create Supabase Database
1. Go to [supabase.com](https://supabase.com)
2. Create free account and new project
3. Note your database URL from Settings > Database

### Step 2: Export Current Data
```bash
# Run this in Replit terminal before migration
pg_dump $DATABASE_URL > backup.sql
```

### Step 3: Setup GitHub Repository
1. Create new GitHub repository
2. Push all your code files to GitHub
3. Include: main.py, app.py, routes.py, models.py, study_plan_generator.py, templates/, static/

### Step 4: Deploy to Render
1. Go to [render.com](https://render.com)
2. Create account and "New Web Service"
3. Connect your GitHub repository
4. Configure:
   - Build Command: `pip install -r requirements.txt` 
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT main:app`

### Step 5: Set Environment Variables in Render
```
DATABASE_URL=your_supabase_database_url
FIREBASE_API_KEY=AIzaSyCM4RqLyKdm8pcQwqRuEVlieP3epYKyPLI
FIREBASE_PROJECT_ID=prepmate-2dfa5
FIREBASE_APP_ID=1:1001637355899:web:21b94953cd1c820d211dde
FIREBASE_SERVICE_ACCOUNT_KEY=your_service_account_json
SESSION_SECRET=your_secret_key
```

### Step 6: Import Your Data
```bash
# Connect to new Supabase database and run:
psql your_supabase_url < backup.sql
```

### Step 7: Update Firebase Authorized Domains
Add your new Render URL to Firebase console: `yourapp.onrender.com`

## Option 2: Render + Neon Database

Same steps as above, but use [neon.tech](https://neon.tech) instead of Supabase.

## Option 3: All-Render Solution

If you prefer everything in one place:
- Render Web Service (Free)
- Render PostgreSQL Database ($7/month after 90 days)

## Cost Summary

### Free Forever Option:
- Render Web Service: $0
- Supabase/Neon Database: $0
- Total: $0/month

### Render Complete:
- Render Web Service: $0
- Render Database: $0 (90 days), then $7/month
- Total: $7/month after trial

## Files to Include in GitHub

Essential files for migration:
- main.py
- app.py  
- routes.py
- models.py
- study_plan_generator.py
- templates/ (all HTML files)
- static/ (CSS, JS files)
- requirements.txt (create from current packages)

## Requirements.txt Contents
```
flask==3.0.0
flask-sqlalchemy==3.1.1
flask-cors==4.0.0
firebase-admin==6.4.0
gunicorn==23.0.0
psycopg2-binary==2.9.9
sqlalchemy==2.0.25
werkzeug==3.0.1
email-validator==2.1.0
```

## Testing Migration

After deployment:
1. Visit your new Render URL
2. Test Google sign-in
3. Rate some topics
4. Generate a study plan
5. Verify data persists in your external database

## Backup Strategy

Always keep:
- SQL backup of your data
- GitHub repository with latest code
- Environment variables documented securely

Your app is designed to be completely portable - the migration should be seamless!