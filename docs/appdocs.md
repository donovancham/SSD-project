# Flask Application

## Environment variables
- Development
  - Environment Variables
    - The `python-dotenv` module is used to get local environment variables
    - `.env` file is configured and added to `.gitignore`
  - Secrets
    - Configured using `docker secret`
- Production
  - Jenkins CI is used to configure secrets and environment variables
  - Environment requirements are referenced from the `.env` file