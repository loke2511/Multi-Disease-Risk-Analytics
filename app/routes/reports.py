"""
Reports Routes - PDF Generation and Download
"""
from flask import Blueprint, send_file, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app.models.prediction import Prediction
from app.services.pdf_service import PDFService
import os

reports_bp = Blueprint('reports', __name__)
pdf_service = PDFService()


@reports_bp.route('/generate/<int:prediction_id>')
@login_required
def generate_report(prediction_id):
    """Generate PDF report for a prediction"""
    try:
        prediction = Prediction.query.filter_by(
            id=prediction_id,
            user_id=current_user.id
        ).first_or_404()
        
        # Generate PDF
        pdf_path = pdf_service.generate_report(prediction, current_user)
        
        # Update prediction record
        prediction.report_generated = True
        prediction.report_path = pdf_path
        from app import db
        db.session.commit()
        
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=f"report_{prediction.report_id}.pdf",
            mimetype='application/pdf'
        )
    
    except Exception as e:
        flash(f'Error generating report: {str(e)}', 'error')
        return redirect(url_for('predictions.history'))


@reports_bp.route('/download/<int:prediction_id>')
@login_required
def download_report(prediction_id):
    """Download existing PDF report"""
    try:
        prediction = Prediction.query.filter_by(
            id=prediction_id,
            user_id=current_user.id
        ).first_or_404()
        
        if not prediction.report_generated or not prediction.report_path:
            flash('Report not found. Generating new report...', 'info')
            return redirect(url_for('reports.generate_report', prediction_id=prediction_id))
        
        if not os.path.exists(prediction.report_path):
            flash('Report file not found. Generating new report...', 'info')
            return redirect(url_for('reports.generate_report', prediction_id=prediction_id))
        
        return send_file(
            prediction.report_path,
            as_attachment=True,
            download_name=f"report_{prediction.report_id}.pdf",
            mimetype='application/pdf'
        )
    
    except Exception as e:
        flash(f'Error downloading report: {str(e)}', 'error')
        return redirect(url_for('predictions.history'))


@reports_bp.route('/api/status/<int:prediction_id>')
@login_required
def api_report_status(prediction_id):
    """Check report generation status"""
    prediction = Prediction.query.filter_by(
        id=prediction_id,
        user_id=current_user.id
    ).first_or_404()
    
    return jsonify({
        'report_generated': prediction.report_generated,
        'report_id': prediction.report_id,
        'report_path': prediction.report_path
    })
