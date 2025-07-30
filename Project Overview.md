# DSA Study Planner

## Overview

This is a Flask-based web application that generates personalized 7-day Data Structures and Algorithms (DSA) study plans. The application uses Firebase authentication for user management and provides an intelligent study plan generator that creates customized learning paths based on user skill assessments.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a traditional MVC (Model-View-Controller) architecture pattern with a Flask backend and vanilla JavaScript frontend. The system is designed as a monolithic web application with clear separation of concerns between data models, business logic, and presentation layers.

### Backend Architecture
- **Framework**: Flask with SQLAlchemy ORM for database operations
- **Database**: SQLite for development with PostgreSQL compatibility for production
- **Authentication**: Firebase Admin SDK for server-side user verification
- **API Design**: RESTful endpoints for frontend-backend communication

### Frontend Architecture
- **Technology**: Vanilla JavaScript with ES6 modules
- **UI Framework**: Bootstrap 5 with custom dark theme styling
- **Authentication**: Firebase Client SDK for Google OAuth integration
- **State Management**: Class-based JavaScript modules for component state

## Key Components

### 1. Database Models (`models.py`)
- **User**: Stores Firebase UID, email, display name, and timestamps
- **TopicRating**: Tracks user skill levels (1-5 scale) for DSA topics
- **StudyPlan**: Stores generated 7-day study plans as JSON data

### 2. Study Plan Generator (`study_plan_generator.py`)
- Implements greedy algorithms for optimal study plan creation
- Contains predefined DSA topics with difficulty levels, time estimates, and prerequisites
- Prioritizes topics with lower skill ratings for focused learning
- Includes curated practice problems for each topic

### 3. Authentication System
- Firebase integration for Google OAuth authentication
- Server-side token verification using Firebase Admin SDK
- Session management for user state persistence

### 4. Frontend Modules
- **AuthManager**: Handles Firebase authentication flow
- **DashboardManager**: Manages user dashboard data and UI updates
- **TopicManager**: Handles topic selection and skill rating interface

## Data Flow

1. **User Authentication**: Users sign in via Google OAuth through Firebase
2. **Topic Assessment**: Users select DSA topics and rate their skill levels (1-5)
3. **Plan Generation**: The study plan generator processes user ratings using greedy algorithms
4. **Plan Storage**: Generated plans are stored as JSON in the database
5. **Dashboard Display**: Users can view their personalized 7-day study plans and track progress

## External Dependencies

### Authentication
- **Firebase**: Google OAuth integration and user management
- Environment variables required: `FIREBASE_API_KEY`, `FIREBASE_PROJECT_ID`, `FIREBASE_APP_ID`, `FIREBASE_SERVICE_ACCOUNT_KEY`

### Styling and UI
- **Bootstrap 5**: UI framework with custom dark theme
- **Font Awesome**: Icon library for enhanced visual elements

### Deployment
- **Replit compatibility**: Configured with ProxyFix middleware for proper request handling
- **CORS enabled**: Allows cross-origin requests for API endpoints

## Deployment Strategy

The application is configured for deployment on Replit with the following considerations:

### Environment Configuration
- Database URL configurable via `DATABASE_URL` environment variable
- Session secret configurable via `SESSION_SECRET` environment variable
- Firebase credentials loaded from environment variables

### Database Strategy
- Development: SQLite with file-based storage
- Production: PostgreSQL support via SQLAlchemy engine options
- Auto-migration: Tables created automatically on application startup

### Security Measures
- CORS protection for API endpoints
- Firebase token verification for authenticated routes
- SQL injection prevention through SQLAlchemy ORM
- Session management with secure secret keys

The application uses a simple deployment model suitable for educational and development purposes, with clear pathways for scaling to production environments.
