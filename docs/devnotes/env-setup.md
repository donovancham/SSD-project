# Environment Setup
This page details how to setup the environment step-by-step.

# Configure Signed Requests
Follow the [guide](https://medium.com/@petehouston/quick-guide-to-sign-your-git-commits-c11ce58c22e9). 
All Commands (if not stated) are done in windows powershell.

## 1. Install [Git Bash](https://git-scm.com/download/win) and [GPG4Win](https://www.gpg4win.org/)
## 2. Generate GPG Key Pair

```console
# gpg --default-new-key-algo rsa4096 --gen-key

Key Size: 4096
Expiry: No expire
Name: <Github username>
Email: <Github email>

NOTE: To check your git configured email and name
# git config --list
# git config --global --list
# git config user.email
# git config user.name

To set Email and name
# git config --global user.name <name>
# git config --global user.email <email>
```

## 3. Check if key exists

```console
# gpg --list-secret-keys --keyid-format LONG
...
/Users/hubot/.gnupg/secring.gpg
------------------------------------
sec 4096R/3AA5C34371567BD2 2016-03-10 [expires: 2017-03-10]
uid                        Hubot 
ssb 4096R/42B317FD4BA89E7A 2016-03-10
```

## 4. Share public key (Note: `3AA5C34371567BD2` is what you see from the previous step at the first line)

```console
# gpg --send-keys 3AA5C34371567BD2
```

## 5. Export Public Key from Key ID

```console
# gpg --armor --export 3AA5C34371567BD2
-----BEGIN PGP PUBLIC KEY BLOCK-----
KEY_CONTENT....
-----END PGP PUBLIC KEY BLOCK-----
```

- Go to [Settings > SSH and GPG keys](https://github.com/settings/keys) section on Github.
- Click green button to add new GPG Key
- Copy Paste the public key from the command above

## 6. Configure GPG program

**Windows (Git bash)**
```console
# git config --global gpg.program "C:\Program Files (x86)\GnuPG\bin\gpg.exe"
# git config --global user.signingkey 3AA5C34371567BD2
# git config --global commit.gpgsign true

IMPORTANT: Ensure environment variable set
$env:GNUPGHOME='C:\Users\user\AppData\Roaming\gnupg'
```

**Linux**
```console
$ which gpg
/usr/local/bin/gpg
$ git config --global gpg.program "/usr/local/bin/gpg"
```

## 7. (Optional) Disable TTY (if using CLI in IDE like VS Code)

```console
$ echo 'no-tty' >> ~/.gnupg/gpg.conf
```

## 8. Verify
Try committing to git and you should see the `Verified` badge at the side of the commit.

![Verified Example](../images/verify_button.png)



# Python Environment

## Prerequisites
Ensure the following software are installed before continuing.
- `Python 3.8+`
- `pip`
- `venv`

## Configure Python Environment
1. Install `Python 3.8+` in the environment of choice

```console
# Verify Python Install
$ python3 --version
```

2. Ensure that `pip` is installed

```console
$ pip --version
```

3. Create the virtual environment

**Linux**
```console
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

**Windows**
```console
$ py -3.9 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

4. Environment Variables Setup

**Windows**
```console
CMD
$ set FLASK_APP=run.py
$ set FLASK_ENV=development

Powershell
$ $env:FLASK_APP = "cmsapp/__init__.py"
$ $env:FLASK_DEBUG = 1
```

**Linux**
```console
$ export FLASK_APP=cmsapp/__init__.py
$ export FLASK_DEBUG=1
```

5. Start the app with:
- Build containers with names
- Run this in project root

**Development**
```console
$ docker-compose up -d --build
```

**DB Commands**
```console
$ docker-compose exec web python manage.py create_db
```

**Teardown**
```console
$ docker-compose down -v
```

## Install Docker
1. Install [Docker Desktop](https://www.docker.com/)
2. *(Optional)* Install a WSL2 Distro
3. *(Optional)* Configure WSL2 Distro with [Docker Desktop support](https://docs.docker.com/desktop/windows/wsl/)

## Configuration
Follows this guide on [Dockerizing Flask with Postgres, Gunicorn, and Nginx](https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx)

Skip `manage.py` step