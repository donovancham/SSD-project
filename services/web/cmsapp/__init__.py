import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_minify  import Minify
from importlib import import_module
from dotenv import load_dotenv, find_dotenv
from cmsapp.config import config_dict


def register_extensions(app: Flask):
    db.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app: Flask):
    for module_name in ('authentication', 'home'):
        module = import_module('cmsapp.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


# Configure the database
# db: SQLAlchemy = SQLAlchemy(app)
db: SQLAlchemy = SQLAlchemy()

# Configure login manager
login_manager: LoginManager = LoginManager()

# Initialize project with name
app = Flask(__name__)
# Load environment variables from `.env`
load_dotenv(find_dotenv(".env.dev"))

# Init flask app
DEBUG = (os.getenv('CMS_DEBUG', 'False') == 'True')
get_config_mode = 'Debug' if DEBUG else 'Production'

# Load the configuration using the default values
app_config = config_dict[get_config_mode.capitalize()]

app.config.from_object(app_config)
register_extensions(app)
register_blueprints(app)

Migrate(app, db)

if not DEBUG:
    Minify(app=app, html=True, js=False, cssless=False)
else:
    app.logger.info('DEBUG            = ' + str(DEBUG)             )
    app.logger.info('Page Compression = ' + 'FALSE' if DEBUG else 'TRUE' )
    app.logger.info('DBMS             = ' + app_config.SQLALCHEMY_DATABASE_URI)
    app.logger.info('ASSETS_ROOT      = ' + app_config.ASSETS_ROOT )