# Flask Application

## Dependencies
- Flask
- Flask-SQLAlchemy
- psycopg2-binary
- gunicorn
- Flask-Login
- Flask-Migrate
- Flask-Wtf
- email_validator
- Flask-Restx
- Flask-Minify
- python-dotenv

## Environment variables
- Development
  - Environment Variables
    - The `python-dotenv` module is used to get local environment variables
    - `.env` file is configured and added to `.gitignore`
    - Docker environment
- Production
  - Jenkins CI is used to configure secrets and environment variables
  - Environment requirements are referenced from the `.env` file