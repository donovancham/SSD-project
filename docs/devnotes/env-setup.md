# Environment Setup
This page details how to setup the environment step-by-step.

## Configure Signed Requests
Follow the [guide](https://medium.com/@petehouston/quick-guide-to-sign-your-git-commits-c11ce58c22e9). 
All Commands (if not stated) are done in windows powershell.

### 1. Install [Git Bash](https://git-scm.com/download/win) and [GPG4Win](https://www.gpg4win.org/)
### 2. Generate GPG Key Pair

```console
# gpg --default-new-key-algo rsa4096 --gen-key

Key Size: 4096
Expiry: No expire
Name: <Github username>
Email: <Github email>
```

### 3. Check if key exists

```console
# gpg --list-secret-keys --keyid-format LONG
...
/Users/hubot/.gnupg/secring.gpg
------------------------------------
sec 4096R/3AA5C34371567BD2 2016-03-10 [expires: 2017-03-10]
uid                        Hubot 
ssb 4096R/42B317FD4BA89E7A 2016-03-10
```

### 4. Share public key (Note: `3AA5C34371567BD2` is what you see from the previous step at the first line)

```console
# gpg --send-keys 3AA5C34371567BD2
```

### 5. Export Public Key from Key ID

```console
# gpg --armor --export 3AA5C34371567BD2
-----BEGIN PGP PUBLIC KEY BLOCK-----
KEY_CONTENT....
-----END PGP PUBLIC KEY BLOCK-----
```

- Go to [Settings > SSH and GPG keys](https://github.com/settings/keys) section on Github.
- Click green button to add new GPG Key
- Copy Paste the public key from the command above

### 6. Configure GPG program

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

### 7. (Optional) Disable TTY (if using CLI in IDE like VS Code)

```console
$ echo 'no-tty' >> ~/.gnupg/gpg.conf
```

### Verify
Try committing to git and you should see the `Verified` badge at the side of the commit.

![Verified Example](../images/verify_button.png)

## Prerequisites
Ensure the following software are installed before continuing.
- `Python 3.10.7`
- `pip`
- `venv`

## Configure Python Environment
1. Install `Python 3.10.7` in the environment of choice

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
$ . venv/bin/activate
$ pip install -r requirements.txt
```

**Windows**
```console
$ py -3.9 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

## Install Docker
1. Install [Docker Desktop](https://www.docker.com/)
2. *(Optional)* Install a WSL2 Distro
3. *(Optional)* Configure WSL2 Distro with [Docker Desktop support](https://docs.docker.com/desktop/windows/wsl/)

## Running Docker Environment
```console
$ docker-compose up --build
```

## Barebones Flask Dev Environment (Not Tested)
```console
Ensure venv is activated
$ . venv/bin/activate

Run the barebones server
$ flask run --host=0.0.0.0 --port=5000
```