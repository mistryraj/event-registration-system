from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import os

# --- DATABASE SETUP ---
basedir = os.path.abspath(os.path.dirname(__file__))

# --- MOVED TO TOP LEVEL ---
# Initialize the SQLAlchemy database extension
db = SQLAlchemy()

# --- MOVED TO TOP LEVEL: Define the Event Database Model ---
# This class defines the "events" table in our database
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=True)
    event_date = db.Column(db.String(20), nullable=False)
# ------------------------------------------

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_super_secret_key_12345'
    
    # --- DATABASE CONFIG ---
    # We tell Flask where to save our SQLite database file
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'events.db')
    
    # Initialize the app with the database
    db.init_app(app)
    # ---------------------------

    # --- This is our mock (fake) admin user ---
    ADMIN_USERNAME = 'admin'
    ADMIN_PASSWORD = 'password123'
    
    # --- Create the database tables ---
    # This must stay inside the function
    with app.app_context():
        db.create_all()
    # ---------------------------------------

    # --- UPDATED: Student Dashboard ---
    @app.route('/')
    def home():
        """
        This is the main student dashboard.
        It now queries the real database for all events.
        """
        all_events = Event.query.all()
        return render_template('student_dashboard.html', events=all_events)

    @app.route('/admin/login', methods=['GET', 'POST'])
    def admin_login():
        error = None
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                session['admin_logged_in'] = True
                return redirect(url_for('admin_dashboard'))
            else:
                error = 'Invalid username or password'
        
        return render_template('admin_login.html', error=error)

    @app.route('/admin/dashboard')
    def admin_dashboard():
        return render_template('admin_dashboard.html')

    # --- UPDATED: Create Event ---
    @app.route('/admin/event/create', methods=['GET', 'POST'])
    def create_event():
        if request.method == 'POST':
            new_event = Event(
                title=request.form['title'],
                description=request.form['description'],
                event_date=request.form['event_date']
            )
            
            db.session.add(new_event)  # Add to the database session
            db.session.commit()      # Save the changes to the file
            
            return redirect(url_for('admin_dashboard'))
        
        return render_template('create_event.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)