"""
Prediction Routes - Disease Prediction Forms and Results
"""
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models.prediction import Prediction
from app.services.prediction_service import PredictionService
from config import Config

predictions_bp = Blueprint('predictions', __name__)
prediction_service = PredictionService()


@predictions_bp.route('/<disease_type>')
@login_required
def predict_disease(disease_type):
    """Show prediction form for a specific disease"""
    if disease_type not in Config.DISEASES:
        flash('Disease not found.', 'error')
        return redirect(url_for('main.dashboard'))
    
    disease_info = Config.DISEASES[disease_type]
    
    return render_template(
        'predictions/prediction_form.html',
        disease_type=disease_type,
        disease_info=disease_info
    )


@predictions_bp.route('/api/<disease_type>', methods=['POST'])
@login_required
def api_predict(disease_type):
    """API endpoint for disease prediction"""
    try:
        if disease_type not in Config.DISEASES:
            return jsonify({'error': 'Disease not found'}), 404
        
        # Get input features from request
        features = request.get_json() if request.is_json else request.form.to_dict()
        
        if not features:
            return jsonify({'error': 'No input features provided'}), 400
        
        # Make prediction
        result = prediction_service.predict(disease_type, features)
        
        if 'error' in result:
            return jsonify(result), 400
        
        # Save prediction to database
        disease_info = Config.DISEASES[disease_type]
        prediction = Prediction(
            user_id=current_user.id,
            disease_type=disease_type,
            disease_name=disease_info['name'],
            prediction_result=result['prediction'],
            risk_level=result['risk_level'],
            confidence_score=result['confidence'],
            risk_percentage=result['risk_percentage'],
            model_name=result['model_name'],
            model_accuracy=result['model_accuracy']
        )
        
        prediction.set_input_features(features)
        prediction.generate_report_id()
        
        db.session.add(prediction)
        db.session.commit()
        
        # Add prediction ID to result
        result['prediction_id'] = prediction.id
        result['report_id'] = prediction.report_id
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@predictions_bp.route('/result/<int:prediction_id>')
@login_required
def result(prediction_id):
    """Show prediction result"""
    prediction = Prediction.query.filter_by(
        id=prediction_id,
        user_id=current_user.id
    ).first_or_404()
    
    return render_template('predictions/result.html', prediction=prediction)


@predictions_bp.route('/history')
@login_required
def history():
    """Show prediction history"""
    page = request.args.get('page', 1, type=int)
    disease_filter = request.args.get('disease', None)
    risk_filter = request.args.get('risk', None)
    
    query = Prediction.query.filter_by(user_id=current_user.id)
    
    if disease_filter:
        query = query.filter_by(disease_type=disease_filter)
    
    if risk_filter:
        query = query.filter_by(risk_level=risk_filter)
    
    predictions = query.order_by(Prediction.created_at.desc()).paginate(
        page=page,
        per_page=Config.PREDICTIONS_PER_PAGE,
        error_out=False
    )
    
    return render_template(
        'predictions/history.html',
        predictions=predictions,
        diseases=Config.DISEASES
    )


@predictions_bp.route('/delete/<int:prediction_id>', methods=['POST'])
@login_required
def delete_prediction(prediction_id):
    """Delete a prediction"""
    prediction = Prediction.query.filter_by(
        id=prediction_id,
        user_id=current_user.id
    ).first_or_404()
    
    db.session.delete(prediction)
    db.session.commit()
    
    flash('Prediction deleted successfully.', 'success')
    return redirect(url_for('predictions.history'))
