"""
Prediction Model for Storing Disease Prediction History
"""
from datetime import datetime
from app import db
import json


class Prediction(db.Model):
    """Prediction model for storing disease prediction results"""
    
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Disease information
    disease_type = db.Column(db.String(50), nullable=False, index=True)
    disease_name = db.Column(db.String(100), nullable=False)
    
    # Prediction results
    prediction_result = db.Column(db.String(20), nullable=False)  # 'Positive', 'Negative'
    risk_level = db.Column(db.String(20))  # 'Low', 'Medium', 'High'
    confidence_score = db.Column(db.Float)
    risk_percentage = db.Column(db.Float)
    
    # Input features (stored as JSON)
    input_features = db.Column(db.Text)
    
    # Model information
    model_name = db.Column(db.String(100))
    model_version = db.Column(db.String(20))
    model_accuracy = db.Column(db.Float)
    
    # Report
    report_id = db.Column(db.String(50), unique=True, index=True)
    report_generated = db.Column(db.Boolean, default=False)
    report_path = db.Column(db.String(255))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Additional metadata
    notes = db.Column(db.Text)
    
    def set_input_features(self, features_dict):
        """Convert features dictionary to JSON string"""
        self.input_features = json.dumps(features_dict)
    
    def get_input_features(self):
        """Parse JSON string back to dictionary"""
        if self.input_features:
            return json.loads(self.input_features)
        return {}
    
    def generate_report_id(self):
        """Generate a unique report ID"""
        from datetime import datetime
        import hashlib
        
        # Create a unique string based on user, disease, and timestamp
        unique_string = f"{self.user_id}_{self.disease_type}_{datetime.utcnow().timestamp()}"
        hash_object = hashlib.md5(unique_string.encode())
        self.report_id = f"RPT_{hash_object.hexdigest()[:12].upper()}"
    
    def get_risk_color(self):
        """Get color code based on risk level"""
        risk_colors = {
            'Low': '#4CAF50',
            'Medium': '#FF9800',
            'High': '#F44336'
        }
        return risk_colors.get(self.risk_level, '#9E9E9E')
    
    def to_dict(self):
        """Convert prediction to dictionary"""
        return {
            'id': self.id,
            'disease_type': self.disease_type,
            'disease_name': self.disease_name,
            'prediction_result': self.prediction_result,
            'risk_level': self.risk_level,
            'confidence_score': self.confidence_score,
            'risk_percentage': self.risk_percentage,
            'input_features': self.get_input_features(),
            'model_name': self.model_name,
            'model_accuracy': self.model_accuracy,
            'report_id': self.report_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Prediction {self.disease_name} - {self.prediction_result}>'
