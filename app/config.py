import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'edu-crm-secret-key-change-in-prod')
    DEBUG = True