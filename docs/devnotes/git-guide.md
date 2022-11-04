# Git Guide
This guide details how to properly use the `git` tool to get updates from remote or push changes to remote. All code is done in **Git Bash**.

## Project set up steps:

1. Clone project `git clone https://github.com/donovancham/SSD-project.git`
2. Checkout main branch `git checkout main`
3. Create and checkout branch `git checkout -b <branchname>`
4. Push your branch to GitHub `git push -u origin <branchname>`

## Basic workflow:

1. Checkout your branch

```console
$ git checkout <branchname>
```

2. Code and test your code

3. Stage your changes to the branch (best practice to add the files that you modified only) 

```console
$ git add <file name>
```

4. Commit your changes `git commit -m “<commit message>”` or `git commit`. Press enter and type the summary and description for the commit. Then press `esc` and type `:wq`

5. Push your changes to Github with `git push`

## Get updates from main branch to your own branch:

1. Check out main branch `git checkout main`
2. Pull updates from remote main branch to local main branch `git pull`
3. Change back to your branch `git checkout <branchname>`
4. Merge main branch code to your branch `git merge main`

## Once your feature is completed, merge it to main branch

**NOTE:** Ensure Changelog is updated before PR

You can create a pull request in Github to merge your branch to main branch (Please do not commit the merge by yourself).

### OR (NOT ALLOWED)

1. Checkout main branch `git checkout main`
2. Merge your branch to main branch `git merge <branchname>`
3. Push merged code to main branch in Github `git push`

## Stashing
Use this feature when you realise you are working on the wrong branch

```console
Assuming you are on main branch

$ git stash
$ git checkout dev
$ git fetch
$ git pull
$ git checkout -b dev-<feature name>
$ git stash pop
```

## Switch Branches

[Move existing, uncommitted work to a new branch in Git](https://stackoverflow.com/questions/1394797/move-existing-uncommitted-work-to-a-new-branch-in-git)

1. `git stash`
2. `git checkout <branch>`
3. `git stash apply`