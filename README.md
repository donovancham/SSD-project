# Clinic Management System

## Software Requirements
- [Python](https://www.python.org/downloads/release/python-3104/) >= 3.10.4
- [Docker Desktop](https://www.docker.com/) ([WSL2](https://docs.docker.com/desktop/windows/wsl/) is optional but recommended)

## Quickstart
**Windows**
```console
$ cd services\web
$ .\env\Scripts\activate
$ pip install -r requirements.txt
```

**Linux**
```console
$ cd services/web
$ source venv/bin/activate
$ pip install -r requirements.txt
```

**App Dev**
```
$ gunicorn --bind 0.0.0.0:32984 manage:app

OR

$ python manage.py run
```

**Testing**
```console
$ python -m pytest -vv
```

**Development**
```console
$ docker-compose up -d --build
```

**Production**
```console
$ docker-compose -f docker-compose.prod.yml up -d --build
```

Check logs:
```console
$ docker compose -f docker-compose.prod.yml logs -f -t
```

## Docs
- [Initializing Git Repo Setup](docs/devnotes/init.md)
- [Environment Setup Guide](docs/devnotes/env-setup.md)
- [Git Guide](docs/devnotes/git-guide.md)
- [Workflow](docs/devnotes/workflow.md)
- [Task-list](docs/devnotes/tasklist.md)

## Application Architecture
- Project Name: Clinic Management System (CMS)
- Project Link: https://jumpifzer0.me

```sh
├── Jenkinsfile                     # Jenkinsfile used to configure
├── README.md                       # Contains the general documentations
├── docker-compose.prod.yml         # Production docker-compose
├── docker-compose.yml              # Development docker-compose
├── docs                            # Contains the general documentations
│   ├── devnotes                      # Notes for developers
│   │   ├── ...
│   └── images
│       └── verify_button.png
├── services                        # Main web app services
│   ├── certbot                       # Generates HTTPS certs
│   │   └── Dockerfile
│   ├── nginx                         # Reverse proxy container
│   │   ├── Dockerfile
│   │   └── nginx.conf
│   └── web                           # Web app container
│       ├── Dockerfile
│       ├── cmsapp                    # Main Flask application
│       │   ├── __init__.py             # Main application entrypoint
│       │   ├── config.py               # Configuration file
│       │   ├── authentication        # Authentication blueprint
│       │   │   ├── __init__.py
│       │   │   ├── cmsemail.py
│       │   │   ├── cmstoken.py
│       │   │   ├── forms.py
│       │   │   ├── models.py
│       │   │   ├── routes.py
│       │   │   └── util.py
│       │   ├── home                  # General routes
│       │   │   ├── __init__.py
│       │   │   └── routes.py
│       │   ├── static                # Static assets
│       │   │   └── assets
│       │   │       ├── css             # CSS files
│       │   │       │   └── ...           
│       │   │       ├── demo            # Some js files for dashboard
│       │   │       │   └── ...
│       │   │       ├── gulpfile.js
│       │   │       ├── img             # Images
│       │   │       │   └── ...
│       │   │       ├── js              # Other js files
│       │   │       ├── package.json
│       │   │       └── scss            # SCSS files
│       │   ├── templates             # HTML templates
│       │   │   ├── accounts          
│       │   │   │   ├── ...
│       │   │   ├── home
│       │   │   │   ├── ...
│       │   │   ├── includes
│       │   │   │   ├── ...
│       │   │   └── layouts
│       │   │       ├── ...
│       │   └── tests                 # Tests folder
│       │       ├── conftest.py         # Initialize test environment
│       │       ├── functional          # Contains functional tests
│       │       │   ├── ...
│       │       └── unit                # Contains unit tests
│       │           ├── ...
│       ├── entrypoint.sh           # Application entrypoint script for production
│       ├── manage.py               # Enables CLI interaction with app
│       └── requirements.txt        # Requirements for Flask app
└── sonar-project.properties      # Properties for Sonarqube static analysis
```

## Changelog
- v0.0
  - Added Guides for setup
    - `README.md`
    - `docs/devnotes/git-guide.md`
    - `docs/devnotes/init.md`
    - `requirements.txt`
  - Added Workflow Documentations
    - `docs/devnotes/tasklist.md`
    - `docs/devnotes/testing.md`
    - `docs/devnotes/workflow.md`
  - Added Project Documentations
    - `docs/architecture.md`
- v0.1
  - Updated GPG Key generation for verified signature
    - `docs/devnotes/env-setup.md`
  - Updated documentation tasks
    - `docs/devnotes/tasklist.md`
  - Added branch protection documentation
    - `docs/devnotes/workflow.md`
  - Updated codeblocks for accurate depiction of linux/windows code
    - `docs/devnotes/init.md`
    - `README.md`
    - `docs/devnotes/env-setup.md`
- v0.2
  - Added Viewing of Appointment functionality
    - `home/viewAppointment.html`
  - Added Booking of Appointment functionality
    - `home/bookAppointment.html`
  - Added Viewing of Patient Records functionality
    - `home/viewRecords.html`
  - Added Creating of Patient Records functionality
    - `home/createRecords.html`
- v0.3
  - Added Updating of Appointment functionality
    - `home/updateAppointment.html`
  - Added Deleting of Appointment functionality
  - Added Updating of Patient Records functionality
    - `home/updateRecords.html`
  - Added Deleting of Patient Records functionality
- v0.4
  - Added Session control
    - `home/viewAppointment.html`
    - `home/bookAppointment.html`
    - `home/viewRecords.html`
    - `home/createRecords.html`
    - `routes.py`
- v0.5
  - Added password hashing and password salting functionality
    - `accounts/login.html`
    - `accounts /register.html`
- v0.6
  - Added password hashing and 
    - `accounts/login.html`
    - `accounts /register.html`
- v1.0
  - Added basic configuration setup of web stack
    - Copied existing development to `services/web`
    - Migrated existing development processes
      - For these files, `import apps` change to import `cmsapp` (double check pylance for syntax highlighting)
        - `authentication/models.py`
        - `authentication/routes.py`
        - `home/routes.py`
      - Updated as of commit `d7ef544e5c5d9bf8c16b79ecf6779446ed6fb3b0`
    - Using `manage.py` for database updates
      - Run `python manage.py create_db` to create db
      - Run `python manage.py delete_db` to delete db
  - Added documentation for `env-setup`
  - Added documentation of flask app
  - Added documentation for `devnotes/workflow`
    - Added things to note before committing changes
    - Added documentation for how to check the db changes
- v1.1
  - Removed old project work dir `3203ssd`
  - Ported over changes as of commit `7b83cb048221c0870434fb18010f0c6acc71b61b`
    - Added session checking (deny access when not logged in)
    - Added access controls for data access
    - Added appointment booking for nurse
    - Added update functionality for appointment and record creation
  - Added `Jenkinsfile` to mark branch
  - Updated `entrypoint.sh` to use `CMS_DEBUG` environment variable
    - Set such that debug will automatically create a new table
- v1.2
  - Updated `Jenkinsfile`
    - Added basic building and deployment of applcation
    - Added environments
    - Added production deploy script
  - Added `docker-compose.prod.yml`
    - Production configuration to load env vars from deploy env
- v1.3
  - Updated `Jenkinsfile`
    - Deployment working
- v1.3-1
  - Merged latest changes
  - Updated `entrypoint.sh`
    - Fixed the endless waiting error
  - Updated `docker-compose.prod.yml`
    - Removed comments
    - Updated env file names
  - Jenkins deployment test passed
  - To be merged and deployed
  - Added production testing command to `README.md`
- v1.4
  - Added OWASP Dependency checker
  - Re-configured slave agent
    - Live-test (staging deploy before actual deploy)
    - Live-deploy (main deploy)
  - Removed some not updated documentations
- v1.4-1
  - Added Warning next gen plugin to `Jenkinsfile`
  - Added Sonarqube installation into `Jenkinsfile`
- v1.4-2
  - Fixed errors for Warning next gen
  - Added property configuration for sonar-project
  - Added generation of `sonar-report.json` for Warnings next gen
  - Fixed bugs for Sonarqube scanning stage in pipeline
- v1.5
  - Added tests
    - Added unit tests for db models
    - Added functional tests for routes
  - Updated `Jenkinsfile` to publish test results from unit tests