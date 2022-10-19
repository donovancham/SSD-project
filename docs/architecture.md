# Architecture
Documents the general architecture of the project.

## Infrastructure
- Project
  - Docker
    - Python WSGI/ASGI Server (Bjoern)
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

## Folder Structure (TBD)
- /

