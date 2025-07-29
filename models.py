from app import db
from datetime import datetime
import json

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firebase_uid = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    display_name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    topic_ratings = db.relationship('TopicRating', backref='user', lazy=True, cascade='all, delete-orphan')
    study_plans = db.relationship('StudyPlan', backref='user', lazy=True, cascade='all, delete-orphan')

class TopicRating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    topic_name = db.Column(db.String(100), nullable=False)
    skill_level = db.Column(db.Integer, nullable=False)  # 1-5 scale
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class StudyPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plan_data = db.Column(db.Text, nullable=False)  # JSON string of the 7-day plan
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_plan_data(self):
        """Parse the JSON plan data"""
        return json.loads(self.plan_data)
    
    def set_plan_data(self, data):
        """Set the plan data as JSON string"""
        self.plan_data = json.dumps(data)
