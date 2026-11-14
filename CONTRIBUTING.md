
# Contributing Guidelines

This document defines the development workflow, coding standards, and contribution rules for all members of the Adaptive Model Updating project.

All team members are expected to follow these guidelines to maintain code quality, consistency, and smooth collaboration.

## 1. Development Workflow

This project follows GitHub Flow.

The `main` branch contains stable and reviewed code. All new features, fixes, documentation updates, and configuration changes must be developed on separate branches.

### 1.1. Branch Strategy

| Branch | Purpose |
|---|---|
| `main` | Stable and reviewed project code |
| Feature branches | New features and functionality |
| Fix branches | Bug fixes |
| Documentation branches | Documentation updates |
| CI branches | CI/CD configuration |
| Chore branches | Project maintenance and configuration |

### 1.2. Branch Naming Convention

Use the following format:

`<type>/<short-description>`

| Type | Description | Example |
|---|---|---|
| `feat` | New feature | `feat/kafka-ingestion` |
| `fix` | Bug fix | `fix/data-validation` |
| `docs` | Documentation update | `docs/update-readme` |
| `test` | Add or update tests | `test/model-evaluation` |
| `ci` | CI/CD configuration | `ci/setup-github-actions` |
| `chore` | Maintenance and configuration | `chore/bootstrap-project` |
| `refactor` | Code restructuring | `refactor/data-processing` |

Branch names should be short, descriptive, and written in lowercase.

### 1.3. Creating a New Branch

Always create a new branch from the latest `main` branch.

```bash
git switch main
git pull origin main
git switch -c feat/your-feature-name
```

Example:

```bash
git switch main
git pull origin main
git switch -c feat/kafka-ingestion
```

Do not develop new features directly on `main`.

## 2. Commit Convention

The project follows Conventional Commits to maintain a clear and readable Git history.

### 2.1. Commit Message Format

```text
<type>(<scope>): <description>
```

| Type | Description |
|---|---|
| `feat` | Add a new feature |
| `fix` | Fix a bug |
| `docs` | Update documentation |
| `test` | Add or update tests |
| `ci` | Modify CI/CD configuration |
| `chore` | Maintenance and configuration |
| `refactor` | Refactor existing code |
| `perf` | Improve performance |

### 2.2. Commit Message Examples

```text
feat(ingest): add Kafka producer

feat(drift): implement PSI detection

fix(models): correct model evaluation logic

docs(infra): update Docker setup guide

test(drift): add ADWIN unit tests

ci(github): configure automated testing

chore(repo): initialize project structure
```

Commit messages should:
- Describe the actual changes.
- Use clear and concise language.
- Identify the affected module through the scope.
- Avoid vague descriptions such as `update`, `fix code`, or `changes`.

## 3. Pull Request Guidelines

All code and documentation changes must be submitted through Pull Requests.

Direct pushes to `main` should be avoided.

### 3.1. Before Creating a Pull Request

Contributors must:

- Create a branch from the latest `main`.
- Implement the assigned task.
- Follow the project's coding conventions.
- Run relevant tests.
- Check code formatting and linting.
- Update documentation when necessary.
- Ensure no sensitive information is included.

### 3.2. Pull Request Requirements

Every Pull Request should:

- Have a clear and descriptive title.
- Explain the purpose of the changes.
- Describe the main modifications.
- Include testing information.
- Identify potential impacts on other modules.
- Reference related issues or tasks when applicable.

### 3.3. Review Requirements

- Each Pull Request must receive approval from at least one other team member before merging.
- Contributors must address relevant review comments.
- Required CI checks must pass.
- Changes affecting shared interfaces must be documented.
- The author should not approve their own Pull Request.

### 3.4. Merge Strategy

Use the repository's configured merge strategy.

Squash and Merge is preferred for feature branches when appropriate, as it keeps the `main` branch history clean.

## 4. Python Coding Standards

Python code must follow the project's shared configuration in `pyproject.toml`.

The project standardizes on Python 3.11.

### 4.1. Code Style

- Use meaningful variable, function, and class names.
- Follow PEP 8 conventions.
- Use consistent indentation.
- Keep functions focused on a single responsibility.
- Avoid unnecessary code duplication.
- Use type hints for important functions and interfaces.
- Add docstrings to important functions and classes.
- Handle exceptions appropriately.
- Avoid hard-coded credentials and machine-specific paths.

### 4.2. Code Quality Tools

The project uses Ruff for linting and formatting.

Check code quality:

```bash
ruff check .
```

Automatically fix supported lint issues:

```bash
ruff check . --fix
```

Format Python files:

```bash
ruff format .
```

Check formatting without modifying files:

```bash
ruff format --check .
```

## 5. Pre-commit Rules

Pre-commit is used to execute configured code quality checks before each commit.

Install the Git hooks:

```bash
pre-commit install
```

Run all configured hooks manually:

```bash
pre-commit run --all-files
```

Contributors should resolve all relevant hook failures before committing their changes.

## 6. Testing Guidelines

The project uses Pytest for automated testing.

Run the complete test suite:

```bash
pytest -v
```

Run tests with a concise summary:

```bash
pytest -q
```

### 6.1. Testing Responsibilities

Contributors should provide appropriate tests for new or modified functionality.

Depending on the module, testing may include:

| Test Type | Purpose |
|---|---|
| Unit Testing | Validate individual functions and components |
| Data Validation | Check data types, schemas, and missing values |
| Integration Testing | Verify communication between modules |
| Model Testing | Evaluate model behavior and predictions |
| Pipeline Testing | Verify data and workflow execution |

Tests should be placed in the `tests/` directory and follow the naming convention `test_*.py`.

## 7. Data and Model Management

Data and model artifacts must be managed carefully to maintain reproducibility and protect project information.

### 7.1. Data Management

- Do not commit confidential, personal, or sensitive datasets.
- Do not commit large production datasets to Git.
- Use `data/sample/` for small, non-sensitive sample datasets.
- Document data schemas and feature definitions.
- Preserve relevant timestamps and data provenance.
- Record dataset versions when preparing training and evaluation data.

### 7.2. Model Management

- Record relevant model parameters and evaluation metrics.
- Keep track of training dataset versions.
- Evaluate candidate models before deployment.
- Maintain a reference to the currently approved model.
- Document model updates and version changes.
- Support rollback when an updated model fails validation or production checks.

## 8. Data and Service Contracts

The project uses shared technical contracts to define communication between components and development teams.

The contracts are maintained in:

`docs/CONTRACTS.md`

Contributors must update the contracts document when modifying shared interfaces, including:

- Input and output data schemas.
- Kafka topic names and message formats.
- Feature names and data types.
- Model input and output interfaces.
- API request and response formats.
- Infrastructure service names and connection settings.

Before making a breaking change:

1. Notify the affected team.
2. Describe the proposed interface change.
3. Update `docs/CONTRACTS.md`.
4. Coordinate integration and compatibility testing.

## 9. Security and Configuration

- Never commit API keys, passwords, access tokens, or private credentials.
- Use environment variables for sensitive configuration.
- Keep `.env` files out of Git.
- Provide `.env.example` when documenting required environment variables.
- Do not expose production credentials in source code or documentation.
- Avoid committing local machine configuration and virtual environments.

## 10. Continuous Integration

GitHub Actions is used to validate changes automatically.

The initial CI workflow includes:

- Python environment setup.
- Dependency installation.
- Ruff lint checks.
- Ruff formatting checks.
- Pytest execution.

CI checks must pass before a Pull Request is considered ready for merging.

If CI fails, contributors are responsible for investigating and fixing the reported errors.

## 11. Team Collaboration Responsibilities

Every team member is responsible for:

- Working on assigned tasks and modules.
- Following the shared Git workflow.
- Maintaining code quality.
- Writing or updating appropriate tests.
- Keeping documentation up to date.
- Communicating interface changes to affected teams.
- Reviewing Pull Requests from other members.
- Supporting integration and debugging activities.

Each team member must contribute at least one reviewed and merged Pull Request as required by the initial project task.

## 12. Standard Contribution Workflow

The complete contribution process is summarized below.

```text
1. Update local main branch
          |
          v
2. Create a feature branch
          |
          v
3. Implement assigned changes
          |
          v
4. Run Ruff and Pytest
          |
          v
5. Commit changes
          |
          v
6. Push branch to GitHub
          |
          v
7. Create Pull Request
          |
          v
8. GitHub Actions runs CI
          |
          v
9. Code review by another member
          |
          v
10. Resolve review comments
          |
          v
11. Merge approved changes into main
```

