import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables from `.env`
load_dotenv(find_dotenv(".env.dev"))

class Config(object):

    # Set up the App SECRET_KEY
    SECRET_KEY = os.getenv('SECRET_KEY')
    print(SECRET_KEY)

    # Set up main static assets folder
    ASSETS_ROOT = os.getenv('ASSETS_ROOT')
    print(ASSETS_ROOT)  
    

class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

    # PostgreSQL database
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
        os.getenv('DB_ENGINE'),
        os.getenv('DB_USERNAME'),
        os.getenv('DB_PASS'),
        os.getenv('DB_HOST'),
        os.getenv('DB_PORT'),
        os.getenv('DB_NAME')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('APP_MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('APP_MAIL_PASSWORD')

    SERVER_NAME = os.getenv('SERVER_NAME')

class DebugConfig(Config):
    DEBUG = True
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    # This will create a file in `cmsapp` FOLDER
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug'     : DebugConfig
}
