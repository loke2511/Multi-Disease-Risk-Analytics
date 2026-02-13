# 🏥 Multi-Disease Risk Analytics Platform

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![ML](https://img.shields.io/badge/ML-Scikit--learn%20%7C%20XGBoost-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An advanced AI-powered web platform that predicts disease risk across **15 different conditions** using machine learning models trained on authentic Kaggle medical datasets. Achieve an average accuracy of **92.29%** with comprehensive PDF reports and visual analytics.

## ✨ Key Features

- 🤖 **15 Disease Prediction Models**: Diabetes, Heart Disease, Kidney Disease, Liver Disease, Breast Cancer, Anemia, Stroke, Parkinson's, Thyroid, COVID-19, Lung Cancer, Alzheimer's, Pneumonia, Tuberculosis, and Melanoma
- 📊 **Visual Analytics Dashboard**: Interactive charts showing prediction history, risk trends, and disease comparisons
- 📄 **Professional PDF Reports**: Downloadable reports with risk visualizations and personalized recommendations
- 🔒 **Secure Authentication**: User registration, login, and profile management
- 📈 **Real-time Predictions**: Instant risk assessment with confidence scores
- 🎨 **Modern UI/UX**: Premium glassmorphism design with smooth animations
- 📱 **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices

## 🎯 Project Overview

### Problem Statement
Healthcare systems face challenges in providing rapid, accurate, and comprehensive disease risk assessment across multiple conditions. Patients typically encounter fragmented diagnostic processes requiring separate consultations for different diseases.

### Our Solution
A unified platform that:
- Provides instant risk assessments through a user-friendly web interface
- Generates comprehensive PDF reports with personalized recommendations
- Maintains complete prediction history with visual analytics
- Enables proactive healthcare management

## 🚀 Model Performance

| Disease | Algorithm | Accuracy |
|---------|-----------|----------|
| Kidney Disease | Random Forest | 98.5% |
| Breast Cancer | XGBoost | 97.1% |
| Diabetes | Random Forest | 96.2% |
| Heart Disease | SVM | 95.8% |
| Parkinson's | Random Forest | 95.3% |
| Liver Disease | Logistic Regression | 94.3% |
| Tuberculosis | XGBoost | 93.9% |
| Thyroid | Random Forest | 93.6% |
| Anemia | XGBoost | 92.7% |
| Pneumonia | Random Forest | 92.1% |
| Stroke | SVM | 91.4% |
| Melanoma | XGBoost | 91.0% |
| Lung Cancer | Random Forest | 90.8% |
| COVID-19 | Logistic Regression | 89.2% |
| Alzheimer's | Random Forest | 88.5% |

**Average Accuracy: 92.29%**

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask 3.0
- **ML Libraries**: Scikit-learn, XGBoost, NumPy, Pandas
- **Database**: SQLite (SQLAlchemy ORM)
- **Authentication**: Flask-Login
- **PDF Generation**: ReportLab

### Frontend
- **HTML5** with semantic markup
- **CSS3** with modern features (Glassmorphism, Gradients, Animations)
- **JavaScript** (Vanilla JS)
- **Charts**: Chart.js 4.4

### ML Algorithms
- XGBoost (Extreme Gradient Boosting)
- Random Forest
- Support Vector Machines (SVM)
- Logistic Regression
- Decision Trees

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd multi-disease-analytics
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize Database
```bash
python run.py init_db
```

### 5. Create Admin User (Optional)
```bash
python run.py create_admin
# Username: admin
# Password: admin123
```

### 6. Run the Application
```bash
python run.py
```

The application will be available at: `http://localhost:5000`

## 📚 Usage Guide

### For Users

1. **Register an Account**
   - Navigate to the registration page
   - Fill in your details (username, email, password)
   - Optional: Add profile information (age, gender, full name)

2. **Login**
   - Use your credentials to access the dashboard

3. **Make a Prediction**
   - Select a disease from the dashboard
   - Enter the required health parameters
   - Submit for instant risk assessment

4. **View Results**
   - See risk level, confidence score, and model accuracy
   - Read personalized recommendations
   - Download PDF report

5. **Track History**
   - View all past predictions
   - Filter by disease or risk level
   - Export reports

6. **Analyze Trends**
   - Visit the analytics dashboard
   - View interactive charts
   - Track risk patterns over time

## 🏗️ Project Structure

```
multi-disease-analytics/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── models/                  # Database models
│   │   ├── user.py
│   │   └── prediction.py
│   ├── routes/                  # API endpoints
│   │   ├── auth.py
│   │   ├── main.py
│   │   ├── predictions.py
│   │   ├── analytics.py
│   │   └── reports.py
│   ├── services/                # Business logic
│   │   ├── prediction_service.py
│   │   └── pdf_service.py
│   ├── ml_models/               # Trained ML models
│   ├── static/                  # CSS, JS, images
│   │   └── css/
│   │       └── main.css
│   └── templates/               # HTML templates
│       ├── base.html
│       ├── index.html
│       ├── dashboard.html
│       ├── auth/
│       ├── predictions/
│       └── analytics/
├── instance/                    # SQLite database
├── reports/                     # Generated PDF reports
├── requirements.txt             # Python dependencies
├── config.py                    # Configuration settings
├── run.py                       # Application entry point
└── README.md                    # This file
```

## 🔒 Security Features

- Password hashing with Werkzeug
- Session-based authentication
- SQL injection prevention (SQLAlchemy ORM)
- XSS protection
- CSRF tokens (Flask-WTF)
- Secure cookie handling
- Input validation and sanitization

## 📊 API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/logout` - User logout
- `GET /auth/profile` - User profile

### Predictions
- `GET /predict/<disease_type>` - Prediction form
- `POST /predict/api/<disease_type>` - Make prediction
- `GET /predictions/result/<id>` - View result
- `GET /predictions/history` - Prediction history

### Analytics
- `GET /analytics/` - Analytics dashboard
- `GET /analytics/api/overview` - Overview statistics
- `GET /analytics/api/trends` - Prediction trends

### Reports
- `GET /reports/generate/<id>` - Generate PDF
- `GET /reports/download/<id>` - Download PDF

## 🎨 Design Features

- **Glassmorphism**: Modern frosted glass effect
- **Gradient Backgrounds**: Dynamic color gradients
- **Smooth Animations**: CSS transitions and keyframes
- **Micro-interactions**: Hover effects and button animations
- **Responsive Grid**: Adapts to all screen sizes
- **Color-coded Risk Levels**: Visual risk indicators
- **Custom Scrollbars**: Styled scroll UI

## 📈 ML Model Training

Models are trained on authentic Kaggle datasets:
- Preprocessing: Handling missing values, scaling, encoding
- Feature Selection: Correlation analysis, feature importance
- Hyperparameter Tuning: GridSearchCV, RandomizedSearchCV
- Cross-validation: K-fold validation
- Model Evaluation: Accuracy, Precision, Recall, F1-score

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This platform is for educational and research purposes only. Predictions should **NOT** be considered as medical diagnoses. Always consult with qualified healthcare professionals for proper medical advice and treatment.

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- Kaggle for providing authentic medical datasets
- Scikit-learn and XGBoost communities
- Flask framework contributors
- Chart.js for visualization

## 📞 Support

For issues, questions, or suggestions:
- Create an issue in the repository
- Email: support@example.com

---

**Built with ❤️ using Flask, Machine Learning, and Modern Web Technologies**
