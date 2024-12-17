from flask import Flask
from app.models import db
from flask_migrate import Migrate

from app.controllers.owner_controller import owner_bp

from app.controllers.pet_controller import pet_bp

from app.controllers.pettype_controller import pettype_bp

from app.controllers.vet_controller import vet_bp

from app.controllers.specialty_controller import specialty_bp

from app.controllers.visit_controller import visit_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')
    db.init_app(app)
    migrate = Migrate(app, db)  # Initialize Flask-Migrate

    # Register blueprints
    
    app.register_blueprint(owner_bp, url_prefix='/api/owners')
    
    app.register_blueprint(pet_bp, url_prefix='/api/pets')
    
    app.register_blueprint(pettype_bp, url_prefix='/api/pettypes')
    
    app.register_blueprint(vet_bp, url_prefix='/api/vets')
    
    app.register_blueprint(specialty_bp, url_prefix='/api/specialtys')
    
    app.register_blueprint(visit_bp, url_prefix='/api/visits')
    

    with app.app_context():
        db.create_all()

    return app