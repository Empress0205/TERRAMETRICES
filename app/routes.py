from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, current_user, login_required
from app import app
from app.models import User,db
import os
import json
import requests
import google_auth_oauthlib.flow
from google_auth_oauthlib import flow

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
        email = request.form['email']
        password = request.form['password']
        hashed_password = User.hash_password(password)

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Username or email already exists', 'error')
            return render_template('signup.html')

        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('User created successfully', 'success')

        return redirect(url_for('login')) 

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
# Load Google OAuth Config
with open('client_secrets.json', 'r') as file:
    oauth_config = json.load(file)

oauth_flow = google_auth_oauthlib.flow.Flow.from_client_config(
    oauth_config,
    scopes=[
        "https://www.googleapis.com/auth/userinfo.email",
        "openid",
        "https://www.googleapis.com/auth/userinfo.profile",
    ]
)

# Google Signup Route
@app.route('/signup_google')
def signup_google():
    oauth_flow.redirect_uri = "http://127.0.0.1:5000/callback"
    authorization_url, state = oauth_flow.authorization_url()
    session['state'] = state
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    if 'state' not in session or session['state'] != request.args.get('state'):
        return 'Invalid state parameter', 400
    
    oauth_flow.fetch_token(authorization_response=request.url.replace('http:', 'https:'))
    session['access_token'] = oauth_flow.credentials.token
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('home'))  # ✅ Redirect to home
