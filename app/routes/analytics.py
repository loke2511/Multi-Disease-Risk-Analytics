"""
Analytics Routes - Dashboard and Statistics
"""
from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from app.models.prediction import Prediction
from sqlalchemy import func, extract
from app import db
from datetime import datetime, timedelta

analytics_bp = Blueprint('analytics', __name__)


@analytics_bp.route('/')
@login_required
def dashboard():
    """Analytics dashboard"""
    return render_template('analytics/dashboard.html')


@analytics_bp.route('/api/overview')
@login_required
def api_overview():
    """Get analytics overview data"""
    total_predictions = Prediction.query.filter_by(user_id=current_user.id).count()
    
    # Count predictions by risk level
    risk_counts = db.session.query(
        Prediction.risk_level,
        func.count(Prediction.id)
    ).filter_by(user_id=current_user.id).group_by(Prediction.risk_level).all()
    
    risk_distribution = {
        'Low': 0,
        'Medium': 0,
        'High': 0
    }
    for risk, count in risk_counts:
        if risk:
            risk_distribution[risk] = count
    
    # Count predictions by disease
    disease_counts = db.session.query(
        Prediction.disease_name,
        func.count(Prediction.id)
    ).filter_by(user_id=current_user.id).group_by(Prediction.disease_name).all()
    
    disease_distribution = {disease: count for disease, count in disease_counts}
    
    # Recent activity (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_predictions = Prediction.query.filter(
        Prediction.user_id == current_user.id,
        Prediction.created_at >= thirty_days_ago
    ).count()
    
    return jsonify({
        'total_predictions': total_predictions,
        'risk_distribution': risk_distribution,
        'disease_distribution': disease_distribution,
        'recent_predictions': recent_predictions
    })


@analytics_bp.route('/api/trends')
@login_required
def api_trends():
    """Get prediction trends over time"""
    # Get predictions for the last 12 months
    twelve_months_ago = datetime.utcnow() - timedelta(days=365)
    
    monthly_predictions = db.session.query(
        extract('year', Prediction.created_at).label('year'),
        extract('month', Prediction.created_at).label('month'),
        func.count(Prediction.id).label('count')
    ).filter(
        Prediction.user_id == current_user.id,
        Prediction.created_at >= twelve_months_ago
    ).group_by('year', 'month').order_by('year', 'month').all()
    
    # Format data for charts
    labels = []
    data = []
    
    for year, month, count in monthly_predictions:
        month_name = datetime(int(year), int(month), 1).strftime('%B %Y')
        labels.append(month_name)
        data.append(count)
    
    return jsonify({
        'labels': labels,
        'data': data
    })


@analytics_bp.route('/api/disease-comparison')
@login_required
def api_disease_comparison():
    """Compare risk levels across different diseases"""
    
    # Get average confidence score by disease
    disease_stats = db.session.query(
        Prediction.disease_name,
        func.avg(Prediction.confidence_score).label('avg_confidence'),
        func.avg(Prediction.risk_percentage).label('avg_risk'),
        func.count(Prediction.id).label('total_predictions')
    ).filter_by(user_id=current_user.id).group_by(Prediction.disease_name).all()
    
    result = []
    for disease, avg_conf, avg_risk, total in disease_stats:
        result.append({
            'disease': disease,
            'average_confidence': round(avg_conf, 2) if avg_conf else 0,
            'average_risk': round(avg_risk, 2) if avg_risk else 0,
            'total_predictions': total
        })
    
    return jsonify(result)


@analytics_bp.route('/api/recent-activity')
@login_required
def api_recent_activity():
    """Get recent prediction activity"""
    recent = Prediction.query.filter_by(
        user_id=current_user.id
    ).order_by(Prediction.created_at.desc()).limit(10).all()
    
    activity = []
    for pred in recent:
        activity.append({
            'id': pred.id,
            'disease': pred.disease_name,
            'result': pred.prediction_result,
            'risk_level': pred.risk_level,
            'date': pred.created_at.strftime('%Y-%m-%d %H:%M')
        })
    
    return jsonify(activity)
