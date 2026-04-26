import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECERT_KEY = os.environ.get('SECERT_KEY') or 'dev-key-very-secert'
    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    pass