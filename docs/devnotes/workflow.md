# Workflow
This documents how the team workflow is like.

## DO THIS BEFORE COMMITS
1. Update dependency requirements
```console
$ cd services/web
$ pip freeze > requirements.txt
```

2. Run static tests
3. Check changes did not break existing features
4. Upload the environment files to discord
5. Do a `git status` to see what has changed and document them in the changelog in `README.md`

## DB commands
```
$ docker-compose exec db psql --username=hello_flask --dbname=hello_flask_dev

psql (13.8)
Type "help" for help.

hello_flask_dev=# \l
                                        List of databases
      Name       |    Owner    | Encoding |  Collate   |   Ctype    |      Access privileges
-----------------+-------------+----------+------------+------------+-----------------------------
 hello_flask_dev | hello_flask | UTF8     | en_US.utf8 | en_US.utf8 |
 postgres        | hello_flask | UTF8     | en_US.utf8 | en_US.utf8 |
 template0       | hello_flask | UTF8     | en_US.utf8 | en_US.utf8 | =c/hello_flask             +
                 |             |          |            |            | hello_flask=CTc/hello_flask
 template1       | hello_flask | UTF8     | en_US.utf8 | en_US.utf8 | =c/hello_flask             +
                 |             |          |            |            | hello_flask=CTc/hello_flask
(4 rows)

hello_flask_dev=# \c hello_flask_dev
You are now connected to database "hello_flask_dev" as user "hello_flask".

hello_flask_dev=# \dt
          List of relations
 Schema | Name  | Type  |    Owner
--------+-------+-------+-------------
 public | users | table | hello_flask
(1 row)

hello_flask_dev=# \q
```

## Roles
1. Project Manager
   - Manages project schedule
   - Scope weekly meetings
   - Take notes for each meeting
   - Setup workflows
     - **CI/CD**
     - **Automation**
     - **Documentation**

2. Code Reviewer
   - At least 2 people designated as reviewer
   - Reviews the code before approving pull requests (PR)
   - Ensure PR checklist **completed** by individual before pushing

3. Developer
   - Write Code
   - Write Tests
   - Write Documentation

4. Designer
   - Follow secure design guidelines to plan the development of the app
   - Create diagrams for better visualization
   - Write report

5. Testing
   - Write tests to ensure code conforms to requirements
   - Scope and design **non-static tests** (dynamic, UI, pentest)
   - Do the tests to ensure QC for pre-releases

## Processes

### Pull Request Checklist
- [ ] Changelog filled up
- [ ] Update the implementation
- [ ] Commit Message = Changelog

### Branch Protection
- [Branch Protection Configuration Guide](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/managing-a-branch-protection-rule)
- Protected Branch (main)
  - Require a pull request before merging
    - Require approvals
  - Require signed commits
    - Users are required to sign their identity using
    - `git config --global commit.gpgsign true`

### Branching
- Main Branch
  - The main branch will be **protected**
  - Only authorized users can merge Pull Requests
  - Branch will be mainly used for production-ready builds
- Dev Branch
  - All development will be committed to this branch
  - Working builds will be committed into this branch
- Side Dev Branch (`dev-<topic>`)
  - Side branches are use for development of features
  - Each feature can be branched into a separate branch
  - When feature is working, commit back into main

### Changelog
- Changes should be written in the changelog
- Versioning does not matter for dev, production requires full number builds (1.0, 2.0)
- File changes should be explained
- Commit message same as changelog (just copy paste)

```md
- v0.1.1
   - Added html templates
      - `apps/templates/home/index.html`
   - Added routes
      - `apps/home/routes.py`
```

### Taskings
- Each major development feature should be classified
- Sub-objectives should be identified if possible
- Tasks are to be updated in [Tasklist](/docs/devnotes/tasklist.md) during each commit