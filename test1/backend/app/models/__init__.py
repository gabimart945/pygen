from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models

from app.models.owner import Owner

from app.models.pet import Pet

from app.models.pettype import PetType

from app.models.vet import Vet

from app.models.specialty import Specialty

from app.models.visit import Visit
