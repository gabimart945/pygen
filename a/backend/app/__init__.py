from flask import Flask
from flask_cors import CORS
from app.models import db
from flask_migrate import Migrate

from app.controllers.owner_controller import owner_bp

from app.controllers.pet_controller import pet_bp

from app.controllers.vet_controller import vet_bp

from app.controllers.visit_controller import visit_bp






def create_app(config_name='default'):
    app = Flask(__name__)

    @app.after_request
    def add_security_headers(response):
        # Prevents Xss attacks
        response.headers["X-Content-Type-Options"] = "nosniff"

        # Uncomment the following lines if HTTPS is enforced
        # Enforce HTTPS (HSTS)
        # response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"

        # Protection against clickjacking attacks
        response.headers["X-Frame-Options"] = "DENY"

        # Prevents MIME-type sniffing
        response.headers["X-Content-Security-Policy"] = "default-src 'self'"

        # Protection against XSS attacks
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # Refferer-Policy header to prevent leaking of sensitive data
        response.headers["Referrer-Policy"] = "no-referrer-when-downgrade"

        # Permissions-Policy header to limit the capabilities of the browser
        # Limits the use of features such as geolocation, camera, microphone, etc.
        response.headers["Permissions-Policy"] = (
            "accelerometer=(), autoplay=(), camera=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), payment=(), usb=()"
        )

        return response

    if config_name == 'testing':
        app.config.from_object('config.TestingConfig')
    else:
        app.config.from_object('config.DevelopmentConfig')

    # Apply CORS with the allowed origins from the configuration
    CORS(app, origins=app.config["CORS_ALLOWED_ORIGINS"])

    db.init_app(app)
    
    migrate = Migrate(app, db)  # Initialize Flask-Migrate

    # Register blueprints
    
    app.register_blueprint(owner_bp, url_prefix='/api/owners')
    
    app.register_blueprint(pet_bp, url_prefix='/api/pets')
    
    app.register_blueprint(vet_bp, url_prefix='/api/vets')
    
    app.register_blueprint(visit_bp, url_prefix='/api/visits')
    
    

    with app.app_context():
        db.create_all()

    return app