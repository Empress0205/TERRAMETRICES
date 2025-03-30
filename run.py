import os
from app import app  # Assuming 'app' is your Flask instance

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Get port from environment or default to 5000
    app.run(host="0.0.0.0", port=port, debug=True)
