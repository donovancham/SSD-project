# Initial Repo Setup Guide
This page details how to setup the git repo. Recommended to use [the easy way](#clone-existing-easiest). If already started working on the project locally, can consider [the hard way](#setting-up-repo-locally).

- [Tutorial](https://www.atlassian.com/git/tutorials/setting-up-a-repository)

## Setting up Repo locally
1. Initialize the local folder

```console 
$ cd <project_folder>
$ git init .
```

2. Configure Remote

```console 
git remote add <shortname> <url>
$ git remote add origin https://github.com/donovancham/SSD-project.git

Update remote data
$ git fetch origin
```

## Clone Existing (Easiest)
`git clone https://github.com/donovancham/SSD-project.git`