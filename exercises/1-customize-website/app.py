
from flask import Flask, jsonify
import os
import socket

app = Flask(__name__)

@app.route("/")
def home():
    hostname = socket.gethostname()

    return f"""
    <html>
        <head>
            <title>CloudTech Solutions</title>
        </head>
        <body>
            <h1>Welcome to CloudTech Solutions</h1>
            <p>Your trusted cloud computing partner.</p>

            <h2>Company Information</h2>
            <p><strong>Company:</strong> CloudTech Solutions</p>
            <p><strong>Address:</strong> 123 Cloud Street, Toronto, ON</p>
            <p><strong>Email:</strong> contact@cloudtech.example</p>

            <h2>Our Services</h2>
            <ul>
                <li>Cloud Infrastructure</li>
                <li>Cloud Migration</li>
                <li>Application Deployment</li>
                <li>Cloud Monitoring and Support</li>
            </ul>

            <h2>Application Information</h2>
            <p><strong>Version:</strong> 1.0</p>
            <p><strong>Technology:</strong> Python Flask</p>
            <p><strong>Container Hostname:</strong> {hostname}</p>

            <hr>
            <p>Deployed using Docker and Kubernetes.</p>
        </body>
    </html>
    """

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "application": "company-website"
    })

@app.route("/info")
def info():
    return jsonify({
        "application": "Company Website",
        "technology": "Python Flask",
        "hostname": socket.gethostname(),
        "environment": os.getenv("APP_ENV", "development")
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
