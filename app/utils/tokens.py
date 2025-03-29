try:
    import jwt
except ImportError:
    print("The 'jwt' library is not installed. Install it using 'pip install PyJWT'.")
from datetime import datetime, timedelta
from flask import current_app

def generate_verification_token(email):
    """Generates a JWT token for email verification"""
    payload = {
        'email': email,
        'exp': datetime.utcnow() + current_app.config.get('JWT_ACCESS_TOKEN_EXPIRES', timedelta(hours=1)),  # Set default expiry
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

def verify_token(token):
    """Verifies JWT token and extracts email"""
    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        return payload['email']
    except jwt.ExpiredSignatureError:
        print("Token has expired")  # Debugging info (remove in production)
        return None
    except jwt.InvalidTokenError:
        print("Invalid token")  # Debugging info (remove in production)
        return None
