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

- Added basic configuration setup of web stack
- Added documentation for `env-setup`
- Added documentation of flask app