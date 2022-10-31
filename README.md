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
```

**Development**
```console
$ docker-compose up -d --build
```

## Docs
- [Initializing Git Repo Setup](docs/devnotes/init.md)
- [Environment Setup Guide](docs/devnotes/env-setup.md)
- [Git Guide](docs/devnotes/git-guide.md)
- [Workflow](docs/devnotes/workflow.md)
- [Task-list](docs/devnotes/tasklist.md)
- [Testing](docs/devnotes/testing.md)
- [Architecture](docs/architecture.md)
- [App Structure Documentation](https://docs.appseed.us/boilerplate-code/flask#codebase-structure)

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