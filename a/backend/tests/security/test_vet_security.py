import pytest
import requests
from app import create_app
from multiprocessing import Process
import time

BASE_URL = "http://127.0.0.1:5000/api/vets/"

def run_app():
    """
    Runs the Flask app. This function must be at the global scope for multiprocessing compatibility.
    """
    app = create_app("testing")  # Cambia "testing" por la configuración de pruebas que uses
    app.run('0.0.0.0', port=5000)


@pytest.fixture(scope="module", autouse=True)
def start_flask_server():
    """
    Starts the Flask application in a separate process.
    """
    process = Process(target=run_app)
    process.start()
    time.sleep(2)  # Espera a que el servidor se inicie

    yield

    process.terminate()
    process.join()

@pytest.fixture(scope="module")
def api_client():
    """Fixture to provide a reusable API client."""
    return requests

def test_cors_headers(api_client):
    response = api_client.options(BASE_URL)
    assert response.status_code == 200, "CORS preflight request failed."
    assert "Access-Control-Allow-Origin" in response.headers, "Missing CORS header."
    assert response.headers["Access-Control-Allow-Origin"] == "http://localhost:3000", "Invalid CORS header value."

# Uncomment the following test if HTTPS is enforced
#def test_hsts_header(api_client):
#    response = api_client.get(BASE_URL)
#    assert "Strict-Transport-Security" in response.headers, "Missing HTTPS enforcement header."
#    assert response.headers["Strict-Transport-Security"] == "max-age=31536000; includeSubDomains; preload", "Invalid HSTS header value."


def test_x_frame_options_header(api_client):
    response = api_client.get(BASE_URL)
    assert "X-Frame-Options" in response.headers, "Missing X-Frame-Options header."
    assert response.headers["X-Frame-Options"] == "DENY", "Invalid X-Frame-Options header value."

def test_x_content_type_options_header(api_client):
    response = api_client.get(BASE_URL)
    assert "X-Content-Type-Options" in response.headers, "Missing X-Content-Type-Options header."
    assert response.headers["X-Content-Type-Options"] == "nosniff", "Invalid X-Content-Type-Options header value."

def test_referrer_policy_header(api_client):
    response = api_client.get(BASE_URL)
    assert "Referrer-Policy" in response.headers, "Missing Referrer-Policy header."
    assert response.headers["Referrer-Policy"] == "no-referrer-when-downgrade", "Invalid Referrer-Policy header value."

def test_permissions_policy_header(api_client):
    response = api_client.get(BASE_URL)
    assert "Permissions-Policy" in response.headers, "Missing Permissions-Policy header."
    assert response.headers["Permissions-Policy"] == "accelerometer=(), autoplay=(), camera=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), payment=(), usb=()", "Invalid Permissions-Policy header value."

def test_sql_injection_protection(api_client):
    
    
    
    
    payload = {"first_name": "' OR '1'='1"}
    response = api_client.post(BASE_URL, json=payload)
    
    assert response.status_code in [400], "SQL Injection not properly handled for field 'first_name'."
    
    
    
    
    payload = {"last_name": "' OR '1'='1"}
    response = api_client.post(BASE_URL, json=payload)
    
    assert response.status_code in [400], "SQL Injection not properly handled for field 'last_name'."
    
    
    

def test_xss_protection(api_client):
    response = api_client.get(BASE_URL)
    assert response.status_code != 500, "Unexpected server error."
    assert "X-Content-Type-Options" in response.headers, "Missing XSS protection header."
    assert response.headers["X-Content-Type-Options"] == "nosniff", "Invalid XSS protection header value."