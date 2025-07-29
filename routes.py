import os
import json
from flask import render_template, request, jsonify, session, redirect, url_for
from app import app, db
from models import User, TopicRating, StudyPlan
from study_plan_generator import StudyPlanGenerator
import firebase_admin
from firebase_admin import credentials, auth
import logging

# Initialize Firebase Admin SDK
try:
    # Try to get service account from environment
    service_account_key = os.environ.get("FIREBASE_SERVICE_ACCOUNT_KEY")
    if service_account_key:
        service_account_info = json.loads(service_account_key)
        cred = credentials.Certificate(service_account_info)
    else:
        # Fallback to default credentials
        cred = credentials.ApplicationDefault()
    
    firebase_admin.initialize_app(cred)
    logging.info("Firebase Admin SDK initialized successfully")
except Exception as e:
    logging.error(f"Failed to initialize Firebase Admin SDK: {e}")

@app.route('/')
def index():
    """Landing page with login option"""
    return render_template(
        'index.html',
        firebase_api_key=os.environ.get("FIREBASE_API_KEY"),
        firebase_project_id=os.environ.get("FIREBASE_PROJECT_ID"),
        firebase_app_id=os.environ.get("FIREBASE_APP_ID"),
    )

@app.route('/dashboard')
def dashboard():
    """User dashboard showing current topics and study plans"""
    return render_template(
        'dashboard.html',
        firebase_api_key=os.environ.get("FIREBASE_API_KEY"),
        firebase_project_id=os.environ.get("FIREBASE_PROJECT_ID"),
        firebase_app_id=os.environ.get("FIREBASE_APP_ID"),
    )

@app.route('/topics')
def topic_selection():
    """Topic selection and skill rating page"""
    return render_template(
        'topic_selection.html',
        firebase_api_key=os.environ.get("FIREBASE_API_KEY"),
        firebase_project_id=os.environ.get("FIREBASE_PROJECT_ID"),
        firebase_app_id=os.environ.get("FIREBASE_APP_ID"),
    )

@app.route('/study-plan')
def study_plan_view():
    """Study plan display page"""
    return render_template(
        'study_plan.html',
        firebase_api_key=os.environ.get("FIREBASE_API_KEY"),
        firebase_project_id=os.environ.get("FIREBASE_PROJECT_ID"),
        firebase_app_id=os.environ.get("FIREBASE_APP_ID"),
    )

@app.route('/api/verify-token', methods=['POST'])
def verify_token():
    """Verify Firebase ID token and create/update user"""
    try:
        data = request.get_json()
        id_token = data.get('idToken') if data else None
        if not id_token:
            return jsonify({'error': 'No token provided'}), 400
        
        # Verify the token
        decoded_token = auth.verify_id_token(id_token)
        firebase_uid = decoded_token['uid']
        email = decoded_token.get('email', '')
        display_name = decoded_token.get('name', '')
        
        # Find or create user
        user = User.query.filter_by(firebase_uid=firebase_uid).first()
        if not user:
            user = User()
            user.firebase_uid = firebase_uid
            user.email = email
            user.display_name = display_name
            db.session.add(user)
            db.session.commit()
        
        # Store user ID in session
        session['user_id'] = user.id
        session['firebase_uid'] = firebase_uid
        
        return jsonify({'success': True, 'user_id': user.id})
    
    except Exception as e:
        logging.error(f"Token verification failed: {e}")
        return jsonify({'error': 'Invalid token'}), 401

@app.route('/api/user-data')
def get_user_data():
    """Get current user's topic ratings and study plans"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get topic ratings
    topic_ratings = {}
    for rating in user.topic_ratings:
        topic_ratings[rating.topic_name] = rating.skill_level
    
    # Get latest study plan
    latest_plan = StudyPlan.query.filter_by(user_id=user_id).order_by(StudyPlan.created_at.desc()).first()
    study_plan = latest_plan.get_plan_data() if latest_plan else None
    
    return jsonify({
        'user': {
            'id': user.id,
            'email': user.email,
            'display_name': user.display_name
        },
        'topic_ratings': topic_ratings,
        'study_plan': study_plan
    })

@app.route('/api/save-ratings', methods=['POST'])
def save_topic_ratings():
    """Save user's topic skill ratings"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        data = request.get_json()
        ratings = data.get('ratings', {}) if data else {}
        
        for topic_name, skill_level in ratings.items():
            # Find existing rating or create new one
            rating = TopicRating.query.filter_by(
                user_id=user_id, 
                topic_name=topic_name
            ).first()
            
            if rating:
                rating.skill_level = skill_level
            else:
                rating = TopicRating()
                rating.user_id = user_id
                rating.topic_name = topic_name
                rating.skill_level = skill_level
                db.session.add(rating)
        
        db.session.commit()
        return jsonify({'success': True})
    
    except Exception as e:
        logging.error(f"Failed to save ratings: {e}")
        return jsonify({'error': 'Failed to save ratings'}), 500

@app.route('/api/generate-plan', methods=['POST'])
def generate_study_plan():
    """Generate a 7-day study plan using greedy algorithm"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        # Get user's topic ratings
        ratings = {}
        topic_ratings = TopicRating.query.filter_by(user_id=user_id).all()
        for rating in topic_ratings:
            ratings[rating.topic_name] = rating.skill_level
        
        if not ratings:
            return jsonify({'error': 'No topic ratings found. Please rate your skills first.'}), 400
        
        # Generate study plan
        generator = StudyPlanGenerator()
        plan_data = generator.generate_plan(ratings)
        
        # Save study plan
        study_plan = StudyPlan()
        study_plan.user_id = user_id
        study_plan.set_plan_data(plan_data)
        db.session.add(study_plan)
        db.session.commit()
        
        return jsonify({'success': True, 'plan': plan_data})
    
    except Exception as e:
        logging.error(f"Failed to generate study plan: {e}")
        return jsonify({'error': 'Failed to generate study plan'}), 500

@app.route('/api/logout', methods=['POST'])
def logout():
    """Clear user session"""
    session.clear()
    return jsonify({'success': True})
