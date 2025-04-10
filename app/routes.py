from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, current_user, login_required
from app import app
from app.models import User, db
import os
import json
import requests
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from google_auth_oauthlib.flow import Flow

# ✅ Home route
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/calculator')
def category_select():
    return render_template('category.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

# ✅ Fixed Signup Route

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '').strip()
            confirm_password = request.form.get('confirm_password', '').strip()
            
            # Validate inputs
            if not all([email, password, confirm_password]):
                flash('All fields are required', 'error')
                return redirect(url_for('signup'))
            
            if password != confirm_password:
                flash('Passwords do not match', 'error')
                return redirect(url_for('signup'))
                
            if len(password) < 8:
                flash('Password must be at least 8 characters', 'error')
                return redirect(url_for('signup'))

            # Rest of your signup logic...
            if User.query.filter_by(email=email).first():
                flash('Email already registered', 'error')
                return redirect(url_for('signup'))

            new_user = User(email=email, verified=False)
            new_user.set_password(password)
            
            db.session.add(new_user)
            db.session.commit()
            
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))

        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Signup error: {str(e)}')
            flash('Account creation failed. Please try again.', 'error')
            return redirect(url_for('signup'))
            
    return render_template('signup.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # If already logged in
        return redirect(url_for('home'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            next_page = request.args.get('next') or url_for('home')  # Safe redirect
            return redirect(next_page)
        else:
            flash('Login failed. Check email/password', 'error')
    
    return render_template('login.html')
# Google OAuth Configuration
with open('client_secrets.json', 'r') as file:
    oauth_config = json.load(file)

# Initialize the OAuth flow
oauth_flow = Flow.from_client_config(
    oauth_config,
    scopes=[
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
    ],
    redirect_uri="http://127.0.0.1:5000/callback"
)

@app.route('/signup_google')
def signup_google():
    authorization_url, state = oauth_flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    session['state'] = state
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    if 'state' not in session or session['state'] != request.args.get('state'):
        return 'Invalid state parameter', 400
    
    try:
        oauth_flow.fetch_token(authorization_response=request.url)
        
        # Get user info from the token
        credentials = oauth_flow.credentials
        id_info = id_token.verify_oauth2_token(
            credentials.id_token,
            google_requests.Request(),
            oauth_config['web']['client_id']
        )
        
        email = id_info['email']
        
        # Check if user exists or create new user
        user = User.query.filter_by(email=email).first()
        if not user:
            # Create new user without password (Google-authenticated users)
            new_user = User(email=email)
            db.session.add(new_user)
            db.session.commit()
            user = new_user
        
        # Log the user in
        login_user(user)
        flash('Logged in successfully with Google!', 'success')
        
        # Redirect to calculator page
        return redirect(url_for('category_select'))
    
    except Exception as e:
        flash('Google authentication failed', 'error')
        app.logger.error(f'Google auth error: {str(e)}')
        return redirect(url_for('signup'))
    
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('home'))  

@app.route('/test-db')
def test_db():
    try:
        test_user = User(email='test@test.com')
        test_user.set_password('test123')
        db.session.add(test_user)
        db.session.commit()
        return "User added successfully!"
    except Exception as e:
        return f"Failed: {str(e)}"
    
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Send password reset email (implement this function)
            # send_password_reset_email(user)
            flash('Password reset email sent!', 'success')
        else:
            flash('Email not found', 'error')
    
    return render_template('forgot-password.html')
