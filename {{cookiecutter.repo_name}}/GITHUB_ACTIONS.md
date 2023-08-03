# Continuous Delivery using GitHub Actions

## Goals

1. Understand Continuous Delivery
2. Know the parts of a CI/CD pipeline for Python packages
3. Have an advanced understanding of GitHub Actions

<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>

## Delivery "Environments"

Dev -> QA/Staging -> Prod

- 0.0.0rc0
- 0.0.0rc1
- 0.0.0a0
- 0.0.0b0

```mermaid
flowchart LR
    Laptop(GitHub Actions)
    TestPyPI(Test PyPI)
    ProdPyPI(Prod PyPI)

    Laptop --> TestPyPI --> ProdPyPI
```

<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
## High-level CI/CD Workflow for Python packages

```mermaid
sequenceDiagram
    actor Developer Laptop
    participant GitHub
    participant GitHub Actions
    participant PyPI

    Developer Laptop->>GitHub: Create branch and open PR
    GitHub->>GitHub Actions: emit event
    GitHub Actions->>GitHub Actions: build and test

    loop Until build passes and PR is approved
        Developer Laptop->>Developer Laptop: Make changes and small commits
        Developer Laptop->>GitHub: Push changes to PR branch
        GitHub->>GitHub Actions: emit event
        GitHub Actions->>GitHub Actions: build and test
    end

    Developer Laptop->>GitHub: Merge PR to main
    GitHub->>GitHub Actions: emit event
    GitHub Actions->>GitHub Actions: build and test
    GitHub Actions->>PyPI: Publish to Test PyPI
    GitHub Actions->>PyPI: Publish to Prod PyPI

```


<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>

## Detailed CI/CD Workflow for Python Packages



```mermaid
sequenceDiagram
    actor Developer Laptop
    participant GitHub
    participant GitHub Actions
    participant Test and Prod PyPI

    Developer Laptop->>Developer Laptop: Creates feature branch

    Developer Laptop->>Developer Laptop: Makes changes and small commits

    Developer Laptop->>GitHub: Pushes feature branch to GitHub: <br/> git push origin feature/<name>

    Developer Laptop->>GitHub: Opens Pull Request

    GitHub->>GitHub Actions: Emits a <br/>pull_request[type=opened, branch=feature/<name>] <br/>event

    GitHub Actions->>GitHub Actions: Reacts to pull_request event by triggering CI/CD workflow:

    GitHub Actions->>GitHub Actions: Run code quality checks: <br/>lint, format, <br/>build wheel, test against wheel, check test coverage, report test coverage,<br/> assert version not taken, <br/>build and test docs, <br/>etc.

    Note right of GitHub Actions: ^^^ the locked requirements file may be <br/>used here if desired.
    GitHub Actions->>Test and Prod PyPI: Publish to *Test* PyPI

    Note right of Developer Laptop: If the worflow passed, <br/> the developer could solicit peer reviews <br/> at this stage. Otherwise they can iterate until <br/> the build *does* pass like so:

    loop Until build passes and PR is approved
        Developer Laptop->>Developer Laptop: [Optionally]<br/> Reacts to feedback from CI or peers. <br/>Make more commits.

        Developer Laptop->>GitHub: Update PR by pushing latest commits to PR branch:<br/> git push origin feature/<name>

        GitHub->>GitHub Actions: Emits a<br/> pull_request[type=synchronize, branch=feature/<name>] <br/>event
        GitHub Actions->>GitHub Actions: Re-runs CI/CD workflow as before...
        GitHub Actions->>Test and Prod PyPI: Publish to Test PyPI
    end

    Note right of Developer Laptop: Once the build (and peer review when desired) <br/>have passed. The developer can merge to main.

    Developer Laptop->>GitHub: Merge PR to main (likely in UI)
    GitHub->>GitHub Actions: Emits a push[type=synchronized, branch=main]<br/> event
    GitHub Actions->>GitHub Actions: Re-runs CI/CD workflow as before...<br/> This is an extra validation to make sure the <br/>merged changes did not "break the build" for main. <br/>If this fails, the main branch should be fixed ASAP.
    GitHub Actions->>GitHub Actions: Tag the commit with the semantic version:<br/> git tag vX.X.X

    Note right of GitHub Actions: [Optionally] require a manual approval before publishing
    GitHub Actions->>GitHub: Push the tag to GitHub:<br/> git push origin main --tags
    GitHub Actions->>Test and Prod PyPI: Publish to Prod PyPI
```



<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>

## GitHub Actions as a Pub-Sub System

```mermaid
graph LR;

    subgraph GitHub_API["GitHub Event Bus / Message Queue"]
        GitHub("GitHub UI/API")
    end

    subgraph Publishers[Publishers / Triggers]
        Dev(Developer)
        Dev -->|git push| GitHub
        Dev -->|Open PR| GitHub
        Dev -->|run workflow| GitHub

        Schedule(CRON Scheduler <br/>in GitHub)
        Schedule -->|schedule| GitHub

        CI(Some Workflow <br/>in GitHub Actions)
        CI -->|git push| GitHub
        CI -->|Open PR| GitHub
        CI -->|Workflow REST API call| GitHub

        Program(Program outside of <br/>GitHub Actions, e.g. <br/> an async REST API <br/>using GitHub Actions <br/>for long-running tasks)
        Program -->|workflow dispatch <br/>REST API call| GitHub
    end

    subgraph Subscribers[Subscribers / Listeners]
        Workflow1(Workflow 1)
        GitHub -->|branch created| Workflow1
        GitHub -->|pull_request| Workflow1
        GitHub -->|workflow_dispatch| Workflow1
        GitHub -->|workflow_call| Workflow1
        GitHub -->|schedule| Workflow1

        Workflow2(Workflow 2)
        GitHub -->|workflow_dispatch| Workflow2
    end
```

Notes:
- Workflows may be in different repositories. A single event might trigger multiple workflows in different repos.



### GitHub Actions with 3rd-Party Subscribers

```mermaid
graph LR;

    subgraph GitHub_API["GitHub Event Bus / Message Queue"]
        GitHub("GitHub UI/API")
    end

    subgraph Publishers[Publishers / Triggers]
        Dev(Developer)
        Dev -->|git push| GitHub
        Dev -->|Open PR| GitHub
        Dev -->|run workflow| GitHub

        Schedule(CRON Scheduler <br/>in GitHub)
        Schedule -->|schedule| GitHub

        CI(Some Workflow <br/>in GitHub Actions)
        CI -->|git push| GitHub
        CI -->|Open PR| GitHub
        CI -->|Workflow REST API call| GitHub

        Program(Program outside of <br/>GitHub Actions, e.g. <br/> an async REST API <br/>using GitHub Actions <br/>for long-running tasks)
        Program -->|workflow dispatch <br/>REST API call| GitHub
    end

    subgraph Subscribers[Subscribers / Listeners]
        GitHub --> ClickUp
        GitHub --> Jira
        GitHub --> Slack
        GitHub --> TravisCI
        GitHub --> Jenkins
        GitHub --> Bitbucket
        GitHub --> GitHubActions["GitHub Actions"]
    end

    subgraph Workflows
        Workflow1(Workflow 1)
        GitHubActions -->|branch created| Workflow1
        GitHubActions -->|pull_request| Workflow1
        GitHubActions -->|workflow_dispatch| Workflow1
        GitHubActions -->|workflow_call| Workflow1
        GitHubActions -->|schedule| Workflow1

        Workflow2(Workflow 2)
        GitHubActions -->|workflow_dispatch| Workflow2
    end
```



<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>


## Version bumping

### Manual

Locally

1. manually edit `version.txt` (and optionally CHANGELOG)
2. ci for PR: fail if version is taken
3. append `rc-<short commit hash>` to `version.txt`

CI

4. `python -m build` picks up `project.version` as N + 1 by reading version.txt because it is marked
   as a dynamic field under `tools.setuptools.dynamic`

Write the Changelog manually.

### With commitizen

Locally

1. cz reads version N from version.txt
2. cz reads commit messages since version N was last written
3. cz computes what sort of version bump it was and computes version N + 1
4. cz writes version N + 1 to version.txt

[Optional] After all this, commitizen can also generate the changelog.

CI

1. git: tags commit with version N + 1 to make sure the version isn't taken; may require new commit message
2. script: appends `rc-<short commit hash>` to version.txt if not run on the main branch
3. `python -m build` picks up `project.version` as N + 1 by reading version.txt because it is marked
   as a dynamic field under `tools.setuptools.dynamic`


Goals for tonight

- [x] publish a package to PyPI locally
- [ ] publish the package from CI
- [ ] find a way to push tags *not* during PR, but yes after merge

Bonus: tests

- [ ] compute test coverage with coverage
- [ ] show coverage in different formats
- [ ] fail if coverage is below a certain threshold
- [ ] compute test coverage even if not all tests pass, or argue why this isn't valuable

Bonus GA

- [x] find a way to print the variables, event, etc. for easy debugging

Publishing to PyPI

Try locally

- sign up for PyPI and Test PyPI
- create a .env file
- create a .gitignore file for .env
- add PYPI_USERNAME and PYPI_PASSWORD to .env
- add TEST_PYPI_USERNAME and TEST_PYPI_PASSWORD to .env
- add twine and build to the dev extra in pyproject.toml
