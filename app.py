from flask import Flask, render_template, request, redirect, url_for, flash, session

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_super_secret_key_12345'

    # --- This is our mock (fake) admin user ---
    ADMIN_USERNAME = 'admin'
    ADMIN_PASSWORD = 'password123'
    
    # --- This is our mock (fake) database for events ---
    # We will just use a simple list to store the events.
    events_db = []
    # --------------------------------------------------

    @app.route('/')
    def home():
        return "Hello, this is the home page."

    @app.route('/admin/login', methods=['GET', 'POST'])
    def admin_login():
        error = None
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                # Store in session that the admin is logged in
                session['admin_logged_in'] = True
                return redirect(url_for('admin_dashboard'))
            else:
                error = 'Invalid username or password'
        
        return render_template('admin_login.html', error=error)

    @app.route('/admin/dashboard')
    def admin_dashboard():
        # This now renders your new dashboard HTML file
        return render_template('admin_dashboard.html')

    # --- NEW CODE FOR STORY SERS-2 ---
    @app.route('/admin/event/create', methods=['GET', 'POST'])
    def create_event():
        # This code runs when the user submits the form (POST)
        if request.method == 'POST':
            # Get data from the form
            new_event = {
                'title': request.form['title'],
                'description': request.form['description'],
                'event_date': request.form['event_date']
            }
            # Add the new event to our fake database
            events_db.append(new_event)
            
            # Print to terminal to show it worked (optional)
            print("New Event Created:", new_event)
            print("All Events:", events_db)
            
            # This makes TEST 2 pass:
            return redirect(url_for('admin_dashboard'))
        
        # This code runs when the user first visits the page (GET)
        # This makes TEST 1 pass:
        return render_template('create_event.html')
    # --- END OF NEW CODE ---

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)