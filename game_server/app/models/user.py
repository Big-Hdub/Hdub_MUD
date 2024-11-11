from gino import Gino
from werkzeug.security import generate_password_hash, check_password_hash
from .db import environment, SCHEMA
from sqlalchemy.sql import func

db = Gino()

class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, default=func.now(), onupdate=func.now())

    @classmethod
    async def create(cls, **kwargs):
        if 'password' in kwargs:
            kwargs['hashed_password'] = generate_password_hash(kwargs.pop('password'))
        return await super().create(**kwargs)

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
        }
