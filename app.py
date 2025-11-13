from flask import Flask, render_template, request, redirect, url_for, flash

def create_app():
    app = Flask(__name__)
    # A secret key is required for sessions and flashing messages
    app.config['SECRET_KEY'] = 'your_super_secret_key_12345'

    # --- This is our mock (fake) admin user ---
    # In a real app, this would be in a database
    ADMIN_USERNAME = 'admin'
    ADMIN_PASSWORD = 'password123'
    # -------------------------------------------

    @app.route('/')
    def home():
        return "Hello, this is the home page."

    @app.route('/admin/login', methods=['GET', 'POST'])
    def admin_login():
        error = None
        
        # This code runs when the user submits the form (POST)
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            
            # This is the logic to check the password
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                # Login is successful. Redirect to the dashboard.
                return redirect(url_for('admin_dashboard'))
            else:
                # Login failed. Show an error.
                error = 'Invalid username or password'
        
        # This code runs when the user first visits the page (GET)
        # It renders the HTML file from the 'templates' folder.
        return render_template('admin_login.html', error=error)

    @app.route('/admin/dashboard')
    def admin_dashboard():
        # This is the page the admin sees after logging in.
        return "Welcome to the Admin Dashboard!", 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)