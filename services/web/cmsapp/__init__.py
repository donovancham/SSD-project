import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_minify  import Minify
from flask_mail import Mail
from importlib import import_module
from dotenv import load_dotenv, find_dotenv
from cmsapp.config import config_dict
from flask_wtf.csrf import CSRFProtect
from flask_authorize import Authorize
from flask_talisman import Talisman

def register_extensions(app: Flask):
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Initialize mail with app for 2FA
    mail.init_app(app)

    # Enable RBAC
    authorize.init_app(app)

def register_blueprints(app: Flask):
    for module_name in ('authentication', 'home'):
        module = import_module('cmsapp.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def configure_database(app):
    
    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()
        

# Configure the database
# db: SQLAlchemy = SQLAlchemy(app)
db: SQLAlchemy = SQLAlchemy()

# Configure login manager
login_manager: LoginManager = LoginManager()
login_manager.session_protection = "strong"

# For 2FA
mail: Mail() = Mail()

# Enable RBAC
authorize = Authorize()

# Initialize project with name
app = Flask(__name__)
# Load environment variables from `.env`
load_dotenv(find_dotenv(".env.dev"))

# Init flask app
# To activate production mode, change CMS_DEBUG to 0
DEBUG = (os.getenv('CMS_DEBUG', '0') == '1')
get_config_mode = 'Debug' if DEBUG else 'Production'

# Enable CSRFProtect
csrf = CSRFProtect(app)

# Enable flask-talisman
# csp = {
#     'default-src':  [
#         '\'self\'',
#         '\'unsafe-inline\'',
#         'stackpath.bootstrapcdn.com',
#         'code.jquery.com',
#         'cdn.jsdelivr.net',
#         'cdnjs.cloudflare.com',

#     ]
# }
# talisman = Talisman(
#     app,
#     content_security_policy=csp,
# )


# Load the configuration using the default values
app_config = config_dict[get_config_mode.capitalize()]

app.config.from_object(app_config)
register_extensions(app)
register_blueprints(app)

# Configure flask-login cookie settings
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

Migrate(app, db)


# Environment Checks

if not DEBUG:
    # Compress app size to run faster
    Minify(app=app, html=True, js=False, cssless=False)
else:
    # Print debugger messages
    app.logger.info('DEBUG            = ' + str(DEBUG)             )
    app.logger.info('Page Compression = ' + 'FALSE' if DEBUG else 'TRUE' )
    app.logger.info('DBMS             = ' + app_config.SQLALCHEMY_DATABASE_URI)
    app.logger.info('ASSETS_ROOT      = ' + app_config.ASSETS_ROOT )

    # Configure db
    configure_database(app)
