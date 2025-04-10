from flask_mail import Message
from flask import current_app, url_for
from app import mail
import logging
import json

def send_verification_email(user):
    """Send email verification link to user with SendGrid"""
    try:
        verification_url = url_for(
            'auth.verify_email_route',
            token=user.get_verification_token(),
            _external=True
        )

        msg = Message(
            subject="Verify Your Email - Action Required",
            sender=current_app.config['MAIL_DEFAULT_SENDER'],  # Must match verified sender
            recipients=[user.email],
            html=f"""
            <h2>Almost there, {user.email}!</h2>
            <p>Please verify your email within 1 hour:</p>
            <p><a href="{verification_url}" style="
                background: #0069ff;
                color: white;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 5px;
                ">Verify Email</a></p>
            <p>Or copy this link:<br>{verification_url}</p>
            """
        )

        # Add important headers to prevent spam filtering
        msg.extra_headers = {
            'X-SMTPAPI': json.dumps({
                'filters': {
                    'clicktrack': {'settings': {'enable': 1}},
                    'opentrack': {'settings': {'enable': 0}}
                }
            })
        }

        with current_app.app_context():
            mail.send(msg)
            logging.info(f"Verification email sent to {user.email}")

        return True
    
    except Exception as e:
        logging.error(f"Failed to send verification email: {str(e)}")
        current_app.logger.error(f"SendGrid error details: {e.args}")
        return False