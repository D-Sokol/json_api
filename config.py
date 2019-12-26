import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'cosine-hedgehog-is-bubbling')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///:memory:')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
