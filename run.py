"""
Application Entry Point
Run this file to start the Multi-Disease Risk Analytics Platform
"""
import os
from app import create_app, db
from app.models.user import User
from app.models.prediction import Prediction

# Get environment or default to development
env = os.environ.get('FLASK_ENV', 'development')
app = create_app(env)


@app.shell_context_processor
def make_shell_context():
    """Make database and models available in Flask shell"""
    return {
        'db': db,
        'User': User,
        'Prediction': Prediction
    }


@app.cli.command()
def init_db():
    """Initialize the database"""
    db.create_all()
    print("Database initialized successfully!")


@app.cli.command()
def create_admin():
    """Create an admin user"""
    from werkzeug.security import generate_password_hash
    
    admin = User(
        username='admin',
        email='admin@example.com',
        password_hash=generate_password_hash('admin123'),
        is_admin=True
    )
    
    db.session.add(admin)
    db.session.commit()
    print("Admin user created successfully!")
    print("Username: admin")
    print("Password: admin123")


if __name__ == '__main__':
    # Ensure instance folder exists
    os.makedirs('instance', exist_ok=True)
    os.makedirs('reports', exist_ok=True)
    os.makedirs('app/ml_models', exist_ok=True)
    
    # Initialize database on first run
    with app.app_context():
        db.create_all()
        print("✓ Database initialized successfully!")
        print("✓ Starting Multi-Disease Risk Analytics Platform...")
        print("✓ Access the app at: http://localhost:5000")
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
