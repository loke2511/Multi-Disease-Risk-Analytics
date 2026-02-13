"""
PDF Service - Generate Professional PDF Reports
"""
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from config import Config


class PDFService:
    """Service for generating PDF reports"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Create custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#34495E'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=12,
            alignment=TA_LEFT
        ))
    
    def generate_report(self, prediction, user):
        """Generate a comprehensive PDF report for a prediction"""
        
        # Create filename
        filename = f"report_{prediction.report_id}.pdf"
        filepath = os.path.join(Config.REPORTS_PATH, filename)
        
        # Ensure directory exists
        os.makedirs(Config.REPORTS_PATH, exist_ok=True)
        
        # Create PDF document
        doc = SimpleDocTemplate(
            filepath,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Build content
        story = []
        
        # Header
        story.append(Paragraph(
            "Multi-Disease Risk Analytics Platform",
            self.styles['CustomTitle']
        ))
        story.append(Spacer(1, 12))
        
        # Report Information
        story.append(Paragraph("Disease Prediction Report", self.styles['CustomHeading']))
        
        report_info = [
            ['Report ID:', prediction.report_id],
            ['Date Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['Patient Name:', user.full_name or user.username],
            ['Patient ID:', f'USER_{user.id:06d}']
        ]
        
        info_table = Table(report_info, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#7F8C8D')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#2C3E50')),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 20))
        
        # Prediction Results
        story.append(Paragraph("Prediction Results", self.styles['CustomHeading']))
        
        # Risk color
        risk_colors_map = {
            'Low': colors.HexColor('#4CAF50'),
            'Medium': colors.HexColor('#FF9800'),
            'High': colors.HexColor('#F44336')
        }
        risk_color = risk_colors_map.get(prediction.risk_level, colors.grey)
        
        results_data = [
            ['Disease:', prediction.disease_name],
            ['Prediction Result:', prediction.prediction_result],
            ['Risk Level:', prediction.risk_level],
            ['Risk Percentage:', f"{prediction.risk_percentage:.2f}%"],
            ['Confidence Score:', f"{prediction.confidence_score:.2f}%"],
        ]
        
        results_table = Table(results_data, colWidths=[2*inch, 4*inch])
        results_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#7F8C8D')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#2C3E50')),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('BACKGROUND', (1, 2), (1, 2), risk_color),
            ('TEXTCOLOR', (1, 2), (1, 2), colors.white),
            ('FONTNAME', (1, 2), (1, 2), 'Helvetica-Bold'),
        ]))
        
        story.append(results_table)
        story.append(Spacer(1, 20))
        
        # Model Information
        story.append(Paragraph("Model Information", self.styles['CustomHeading']))
        
        model_data = [
            ['Model Name:', prediction.model_name or 'ML Classifier'],
            ['Model Accuracy:', f"{prediction.model_accuracy:.2f}%" if prediction.model_accuracy else 'N/A'],
            ['Prediction Date:', prediction.created_at.strftime('%Y-%m-%d %H:%M:%S')],
        ]
        
        model_table = Table(model_data, colWidths=[2*inch, 4*inch])
        model_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#7F8C8D')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#2C3E50')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(model_table)
        story.append(Spacer(1, 20))
        
        # Input Features
        story.append(Paragraph("Input Parameters", self.styles['CustomHeading']))
        
        features = prediction.get_input_features()
        if features:
            # Format feature names nicely
            feature_items = []
            for k, v in features.items():
                # Convert snake_case to Title Case
                label = k.replace('_', ' ').title()
                feature_items.append([label, str(v)])
            
            features_table = Table(feature_items, colWidths=[2.5*inch, 3.5*inch])
            features_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#7F8C8D')),
                ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#2C3E50')),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDC3C7')),
            ]))
            
            story.append(features_table)
        else:
            story.append(Paragraph("No input parameters recorded.", self.styles['CustomBody']))
        
        story.append(Spacer(1, 20))
        
        # Recommendations
        story.append(Paragraph("Recommendations", self.styles['CustomHeading']))
        
        recommendations = self._get_recommendations(prediction)
        for rec in recommendations:
            story.append(Paragraph(f"• {rec}", self.styles['CustomBody']))
        
        story.append(Spacer(1, 30))
        
        # Disclaimer
        disclaimer_style = ParagraphStyle(
            name='Disclaimer',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#95A5A6'),
            alignment=TA_CENTER,
            borderPadding=10
        )
        
        story.append(Paragraph(
            "<b>DISCLAIMER:</b> This report is generated by an AI-based prediction system and should "
            "not be considered as a medical diagnosis. Please consult with a qualified healthcare "
            "professional for proper medical advice and treatment.",
            disclaimer_style
        ))
        
        # Build PDF
        doc.build(story)
        
        return filepath
    
    def _get_recommendations(self, prediction):
        """Get personalized recommendations based on prediction"""
        recommendations = []
        
        if prediction.risk_level == 'High':
            recommendations.extend([
                "Consult with a healthcare professional immediately for proper diagnosis and treatment.",
                "Schedule regular check-ups and monitoring of your health parameters.",
                "Follow prescribed medications and treatment plans strictly.",
                "Maintain detailed health records and share them with your doctor."
            ])
        elif prediction.risk_level == 'Medium':
            recommendations.extend([
                "Schedule a consultation with your healthcare provider to discuss these results.",
                "Monitor your symptoms and health parameters regularly.",
                "Adopt preventive measures and lifestyle modifications as recommended.",
                "Consider additional screening tests if advised by your doctor."
            ])
        else:
            recommendations.extend([
                "Continue maintaining a healthy lifestyle to prevent future health issues.",
                "Schedule regular health check-ups as per standard guidelines.",
                "Stay informed about risk factors associated with this condition.",
                "Maintain a balanced diet and regular exercise routine."
            ])
        
        # Disease-specific recommendations
        disease_specific = {
            'Diabetes': "Monitor blood sugar levels regularly and maintain a balanced diet with controlled carbohydrate intake.",
            'Heart Disease': "Keep your blood pressure and cholesterol in check. Avoid smoking and excessive alcohol consumption.",
            'Kidney Disease': "Stay hydrated, limit salt intake, and avoid medications that may harm kidney function.",
            'Liver Disease': "Avoid alcohol, maintain a healthy weight, and be cautious with medications.",
            'Stroke': "Control blood pressure, manage diabetes if present, and maintain healthy cholesterol levels."
        }
        
        if prediction.disease_name in disease_specific:
            recommendations.append(disease_specific[prediction.disease_name])
        
        return recommendations
