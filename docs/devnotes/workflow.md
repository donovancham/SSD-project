# Workflow
This documents how the team workflow is like.

## Updating Dependency Requirements
Run the following code if you installed any additional dependencies

```sh
pip freeze > requirements.txt
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