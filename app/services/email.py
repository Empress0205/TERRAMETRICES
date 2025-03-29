from flask_mail import Message
from flask import current_app, url_for
from app import mail  # Ensure mail instance is imported

def send_verification_email(user):
    """Send email verification link to user"""
    
    verification_url = url_for(
        'auth.verify_email_route',  # Ensure correct endpoint
        token=user.get_verification_token(), 
        _external=True
    )

    msg = Message(
        "Verify Your Email",
        sender=current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@example.com'),
        recipients=[user.email],
        html=f"""
        <h1>Verify Your Email</h1>
        <p>Click <a href="{verification_url}">here</a> to verify your email.</p>
        <p><small>Link expires in 1 hour.</small></p>
        """
    )

    with current_app.app_context():
        mail.send(msg)  # Use the mail instance
