"""
Application Configuration
"""
import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration"""
    
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production-2024'
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'multi_disease_analytics.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # ML Models
    ML_MODELS_PATH = os.path.join(basedir, 'app', 'ml_models')
    
    # PDF Reports
    REPORTS_PATH = os.path.join(basedir, 'reports')
    
    # Upload limits
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file upload
    
    # Pagination
    PREDICTIONS_PER_PAGE = 20
    
    # Email (optional)
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Disease Information
    DISEASES = {
        'diabetes': {'name': 'Diabetes', 'color': '#FF6B6B', 'features': 8},
        'heart_disease': {'name': 'Heart Disease', 'color': '#E74C3C', 'features': 13},
        'kidney_disease': {'name': 'Kidney Disease', 'color': '#3498DB', 'features': 24},
        'liver_disease': {'name': 'Liver Disease', 'color': '#F39C12', 'features': 10},
        'breast_cancer': {'name': 'Breast Cancer', 'color': '#E91E63', 'features': 30},
        'anemia': {'name': 'Anemia', 'color': '#9C27B0', 'features': 6},
        'stroke': {'name': 'Stroke', 'color': '#D32F2F', 'features': 11},
        'parkinsons': {'name': "Parkinson's Disease", 'color': '#7B1FA2', 'features': 22},
        'thyroid': {'name': 'Thyroid Disease', 'color': '#00BCD4', 'features': 21},
        'covid19': {'name': 'COVID-19', 'color': '#FF5722', 'features': 20},
        'lung_cancer': {'name': 'Lung Cancer', 'color': '#607D8B', 'features': 15},
        'alzheimers': {'name': "Alzheimer's Disease", 'color': '#673AB7', 'features': 18},
        'pneumonia': {'name': 'Pneumonia', 'color': '#2196F3', 'features': 12},
        'tuberculosis': {'name': 'Tuberculosis', 'color': '#009688', 'features': 14},
        'melanoma': {'name': 'Melanoma', 'color': '#795548', 'features': 10}
    }
    
    # Risk Levels
    RISK_LEVELS = {
        'low': {'label': 'Low Risk', 'color': '#4CAF50', 'threshold': 0.33},
        'medium': {'label': 'Medium Risk', 'color': '#FF9800', 'threshold': 0.66},
        'high': {'label': 'High Risk', 'color': '#F44336', 'threshold': 1.0}
    }


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
