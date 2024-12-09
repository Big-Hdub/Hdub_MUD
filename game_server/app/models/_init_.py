# app/models/__init__.py
from gino import Gino
from sqlalchemy.ext.declarative import declarative_base
# Import your models here to ensure they are registered with Base
from .user import User  # Example model import

db = Gino()
Base = declarative_base()
