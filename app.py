from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()

# --- Event Database Model ---
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=True)
    event_date = db.Column(db.String(20), nullable=False)
    
    # --- Relationship to Registrations ---
    registrations = db.relationship('Registration', backref='event', lazy=True)

# --- Registration Database Model ---
class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    student_email = db.Column(db.String(100), nullable=False)
    
    # This is the "foreign key" that links this to an Event
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_super_secret_key_12345'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'events.db')
    
    db.init_app(app)

    ADMIN_USERNAME = 'admin'
    ADMIN_PASSWORD = 'password123'
    
    with app.app_context():
        db.create_all() # This will now create BOTH tables

    @app.route('/')
    def home():
        all_events = Event.query.all()
        return render_template('student_dashboard.html', events=all_events)

    # --- Event Details Page (SERS-5) ---
    @app.route('/event/<int:event_id>')
    def event_details(event_id):
        # Find the event by its ID or show a 404 error
        event = db.get_or_404(Event, event_id)
        return render_template('event_details.html', event=event)

    # --- Registration Page (SERS-6) ---
    @app.route('/register/<int:event_id>', methods=['POST'])
    def register(event_id):
        # Find the event this registration is for
        event = db.get_or_404(Event, event_id)
        
        # Get data from the form
        new_registration = Registration(
            student_name=request.form['name'],
            student_email=request.form['email'],
            event_id=event.id
        )
        
        # Save to database
        db.session.add(new_registration)
        db.session.commit()
        
        # --- Mock Email Confirmation (SERS-7) ---
        print("--- MOCK EMAIL SENT ---")
        print(f"To: {new_registration.student_email}")
        print(f"Subject: Confirmation for {event.title}")
        print(f"Hi {new_registration.student_name}, you are registered!")
        print("-----------------------")
        
        # Redirect to a "success" page
        return redirect(url_for('registration_success'))

    # --- Registration Success Page ---
    @app.route('/register/success')
    def registration_success():
        return render_template('registration_success.html')

    # --- Admin Routes Below ---
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

    @app.route('/admin/event/create', methods=['GET', 'POST'])
    def create_event():
        if request.method == 'POST':
            new_event = Event(
                title=request.form['title'],
                description=request.form['description'],
                event_date=request.form['event_date']
            )
            
            db.session.add(new_event)
            db.session.commit()
            
            return redirect(url_for('admin_dashboard'))
        
        return render_template('create_event.html')

    # --- NEW: Admin View Registrations (SERS-3) ---
    # This is the new function, placed in the correct location
    @app.route('/admin/registrations')
    def admin_registrations():
        # This queries your database for all registrations
        # and joins them with the Event data.
        all_registrations = Registration.query.join(Event).order_by(Event.event_date).all()
        
        # This sends that "live data" to your new HTML page
        return render_template('admin_registrations.html', registrations=all_registrations)
    # -----------------------------------------------

    # This "return app" line MUST be the last line inside create_app()
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)