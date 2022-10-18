# Clinic Management System

## Software Requirements
- [Python](https://www.python.org/downloads/release/python-3104/) >= 3.10.4
- [Docker Desktop](https://www.docker.com/) ([WSL2](https://docs.docker.com/desktop/windows/wsl/) is optional but recommended)

## Quickstart
```sh
# Dev Quickstart
flask run --host=0.0.0.0 --port=5000

# Production Testing
docker-compose up --build
```

## Docs
- [Initializing Git Repo Setup](docs/devnotes/init.md)
- [Environment Setup Guide](docs/devnotes/env-setup.md)
- [Git Guide](docs/devnotes/git-guide.md)
- [Workflow](docs/devnotes/workflow.md)
- [Task-list](docs/devnotes/tasklist.md)
- [Testing](docs/devnotes/testing.md)
- [Architecture](docs/architecture.md)

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