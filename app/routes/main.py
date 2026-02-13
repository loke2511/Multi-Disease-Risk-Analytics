"""
Main Routes - Home, Dashboard, About
"""
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models.prediction import Prediction
from sqlalchemy import func
from app import db

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Landing page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')


@main_bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard with disease selection"""
    from config import Config
    
    # Get user statistics
    total_predictions = current_user.get_prediction_count()
    recent_predictions = current_user.get_recent_predictions(limit=5)
    
    # Get predictions by disease
    predictions_by_disease = db.session.query(
        Prediction.disease_name,
        func.count(Prediction.id).label('count')
    ).filter_by(user_id=current_user.id).group_by(Prediction.disease_name).all()
    
    # Get risk distribution
    risk_distribution = db.session.query(
        Prediction.risk_level,
        func.count(Prediction.id).label('count')
    ).filter_by(user_id=current_user.id).group_by(Prediction.risk_level).all()
    
    diseases = Config.DISEASES
    
    return render_template(
        'dashboard.html',
        diseases=diseases,
        total_predictions=total_predictions,
        recent_predictions=recent_predictions,
        predictions_by_disease=predictions_by_disease,
        risk_distribution=risk_distribution
    )


@main_bp.route('/about')
def about():
    """About page with project information"""
    return render_template('about.html')


@main_bp.route('/contact')
def contact():
    """Contact page"""
    return render_template('contact.html')


@main_bp.route('/diseases')
def diseases():
    """List all diseases"""
    from config import Config
    diseases = Config.DISEASES
    return render_template('diseases.html', diseases=diseases)
