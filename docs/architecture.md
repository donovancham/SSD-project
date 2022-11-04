# Architecture
Documents the general architecture of the project.

## Infrastructure
- Project
  - Docker
    - Python WSGI/ASGI Server (Gunicorn)
      - Python Server for application
      - Runs on **Flask** Backend
    - MySQL DB Server
      - Serves as the database backend for the app
    - Nginx
      - Dedicated HTTP Server
      - Python Server will have reverse proxy configured to point to it
    - Jenkins
      - CI/CD Server
      - Configures the pipeline management
      - Automates deployment tasks
        - Build
        - Testing
- Security Configurations
  - To be done on the DigitalOcean box
  - Logging
  - UFW
  - WAF?

## Flask App Structure
[Source](https://docs.appseed.us/boilerplate-code/flask#codebase-structure)

```sh
services
├── nginx                 
│   ├── Dockerfile          # To initialize nginx container
│   └── nginx.conf          # Config for nginx
└── web             # Initialize venv here
    ├── Dockerfile          # Initialize flask + gunicorn
    ├── cmsapp              # Main application root
    │   ├── __init__.py     # flask app
    │   └── config.py       # configs for app
    ├── entrypoint.sh       # Provision script for docker deployment
    ├── manage.py           # Application commands
    └── requirements.txt    # Requirements
```

```bash
< PROJECT ROOT >
   |
   |-- apps/
   |    |
   |    |-- home/                           # A simple app that serve HTML files
   |    |    |-- routes.py                  # Define app routes
   |    |
   |    |-- authentication/                 # Handles auth routes (login and register)
   |    |    |-- routes.py                  # Define authentication routes  
   |    |    |-- models.py                  # Defines models  
   |    |    |-- forms.py                   # Define auth forms (login and register) 
   |    |
   |    |-- static/
   |    |    |-- <css, JS, images>          # CSS files, Javascripts files
   |    |
   |    |-- templates/                      # Templates used to render pages
   |    |    |-- includes/                  # HTML chunks and components
   |    |    |    |-- navigation.html       # Top menu component
   |    |    |    |-- footer.html           # App Footer
   |    |    |    |-- scripts.html          # Scripts common to all pages
   |    |    |
   |    |    |-- layouts/                   # Master pages
   |    |    |    |-- base-fullscreen.html  # Used by Authentication pages
   |    |    |    |-- base.html             # Used by common pages
   |    |    |
   |    |    |-- accounts/                  # Authentication pages
   |    |    |    |-- login.html            # Login page
   |    |    |    |-- register.html         # Register page
   |    |    |
   |    |    |-- home/                      # UI Kit Pages
   |    |         |-- index.html            # Index page
   |    |         |-- page-404.html         # 404 page
   |    |         |-- *.html                # All other pages
   |    |    
   |  config.py                             # Set up the app
   |    __init__.py                         # Initialize the app
   |
   |-- requirements.txt                     # App Dependencies
   |
   |-- .env                                 # Inject Configuration via Environment
   |-- run.py                               # Start the app - WSGI gateway
   ```