# Deployment Guide

This guide provides step-by-step instructions for deploying the Deutsch-Jozsa Quantum Algorithm project.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Local Development Setup](#local-development-setup)
- [Testing](#testing)
- [Code Quality Checks](#code-quality-checks)
- [Building the Package](#building-the-package)
- [GitHub Deployment](#github-deployment)
- [PyPI Deployment](#pypi-deployment)
- [Continuous Integration](#continuous-integration)

---

## Prerequisites

### Required Software

- Python 3.8 or higher
- Git
- pip (Python package manager)

### Optional Tools

- Virtual environment tool (venv, virtualenv, or conda)
- GitHub account (for repository hosting)
- PyPI account (for package distribution)

---

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/elon00/Quantum-Project2.git
cd Quantum-Project2
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

**Production dependencies:**
```bash
pip install -r requirements.txt
```

**Development dependencies:**
```bash
pip install -r requirements-dev.txt
```

### 4. Install Pre-commit Hooks

```bash
pre-commit install
```

---

## Testing

### Run All Tests

```bash
# Run all tests with coverage
pytest --cov=. --cov-report=html --cov-report=term-missing

# Run specific test file
pytest tests/test_deutsch_jozsa.py -v

# Run integration tests only
pytest tests/test_integration.py -v
```

### Run the Main Program

```bash
python deutsch_jozsa.py
```

Expected output should show successful execution of both constant and balanced function tests.

---

## Code Quality Checks

### Formatting

```bash
# Check formatting
black --check deutsch_jozsa.py tests/

# Apply formatting
black deutsch_jozsa.py tests/
```

### Import Sorting

```bash
# Check import order
isort --check-only deutsch_jozsa.py tests/

# Fix import order
isort deutsch_jozsa.py tests/
```

### Linting

```bash
# Flake8
flake8 deutsch_jozsa.py tests/ --max-line-length=88 --extend-ignore=E203,W503

# Pylint
pylint deutsch_jozsa.py --disable=C0103,R0913,R0914
```

### Type Checking

```bash
mypy deutsch_jozsa.py --ignore-missing-imports
```

### Security Scanning

```bash
# Bandit (security linter)
bandit -r deutsch_jozsa.py

# Safety (dependency vulnerability check)
safety check
```

---

## Building the Package

### 1. Install Build Tools

```bash
pip install build twine
```

### 2. Build Distribution

```bash
python -m build
```

This creates:
- `dist/quantum-deutsch-jozsa-1.0.0.tar.gz` (source distribution)
- `dist/quantum_deutsch_jozsa-1.0.0-py3-none-any.whl` (wheel distribution)

### 3. Check Package

```bash
twine check dist/*
```

### 4. Test Installation Locally

```bash
pip install dist/quantum_deutsch_jozsa-1.0.0-py3-none-any.whl
```

---

## GitHub Deployment

### 1. Initialize Git Repository (if not already done)

```bash
git init
git add .
git commit -m "Initial commit: Professional Deutsch-Jozsa implementation"
```

### 2. Create GitHub Repository

1. Go to https://github.com/new
2. Create repository named `Quantum-Project2`
3. Do NOT initialize with README (we already have one)

### 3. Push to GitHub

```bash
git remote add origin https://github.com/elon00/Quantum-Project2.git
git branch -M main
git push -u origin main
```

### 4. Configure GitHub Secrets (for CI/CD)

Go to repository Settings → Secrets and variables → Actions, and add:

- `CODECOV_TOKEN`: Token from codecov.io (optional)
- `PYPI_API_TOKEN`: Token from PyPI for automated releases (optional)

### 5. Enable GitHub Actions

GitHub Actions will automatically run on:
- Push to main/develop branches
- Pull requests
- Daily scheduled runs

### 6. Create Release

```bash
# Tag the release
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

This triggers the release workflow which:
- Builds the package
- Creates a GitHub release
- Optionally publishes to PyPI

---

## PyPI Deployment

### 1. Create PyPI Account

- Register at https://pypi.org/account/register/
- Verify your email
- Enable 2FA (recommended)

### 2. Create API Token

1. Go to Account Settings → API tokens
2. Create token with scope for this project
3. Save the token securely

### 3. Configure PyPI Credentials

**Option A: Using .pypirc file**

Create `~/.pypirc`:
```ini
[pypi]
username = __token__
password = pypi-YOUR-API-TOKEN-HERE
```

**Option B: Using environment variables**
```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-YOUR-API-TOKEN-HERE
```

### 4. Upload to PyPI

**Test PyPI (recommended first):**
```bash
twine upload --repository testpypi dist/*
```

**Production PyPI:**
```bash
twine upload dist/*
```

### 5. Verify Installation

```bash
pip install quantum-deutsch-jozsa
```

---

## Continuous Integration

### GitHub Actions Workflows

The project includes two main workflows:

#### 1. CI/CD Pipeline (`.github/workflows/ci.yml`)

Runs on every push and pull request:
- **Test**: Runs tests on multiple Python versions and OS
- **Lint**: Code quality checks
- **Security**: Security scanning
- **Build**: Package building
- **Docs**: Documentation generation
- **Integration**: Integration tests
- **Performance**: Performance tests

#### 2. Release Pipeline (`.github/workflows/release.yml`)

Runs on version tags (e.g., `v1.0.0`):
- Creates GitHub release
- Builds distribution packages
- Uploads to PyPI (if configured)

### Monitoring CI/CD

1. Go to repository → Actions tab
2. View workflow runs and logs
3. Check for any failures
4. Review coverage reports

---

## Post-Deployment Checklist

- [ ] All tests passing locally
- [ ] Code quality checks passing
- [ ] Documentation complete and accurate
- [ ] CHANGELOG.md updated
- [ ] Version number updated in setup.py and pyproject.toml
- [ ] Git repository clean (no uncommitted changes)
- [ ] GitHub repository created and pushed
- [ ] GitHub Actions workflows running successfully
- [ ] Package built and tested locally
- [ ] PyPI credentials configured (if publishing)
- [ ] Release created on GitHub
- [ ] Package published to PyPI (if applicable)
- [ ] Installation verified from PyPI

---

## Troubleshooting

### Common Issues

**Issue: Import errors when running tests**
```bash
# Solution: Install in editable mode
pip install -e .
```

**Issue: Pre-commit hooks failing**
```bash
# Solution: Run hooks manually and fix issues
pre-commit run --all-files
```

**Issue: GitHub Actions failing**
```bash
# Solution: Check workflow logs in Actions tab
# Common fixes:
# - Update Python version in workflow
# - Check dependency versions
# - Verify secrets are configured
```

**Issue: PyPI upload fails**
```bash
# Solution: Check credentials and package name
# Ensure package name is unique on PyPI
# Verify API token is valid
```

---

## Maintenance

### Regular Updates

1. **Dependencies**: Update monthly
   ```bash
   pip list --outdated
   pip install --upgrade package-name
   ```

2. **Security**: Run security checks weekly
   ```bash
   safety check
   bandit -r deutsch_jozsa.py
   ```

3. **Tests**: Ensure 80%+ coverage
   ```bash
   pytest --cov=. --cov-report=term-missing
   ```

### Version Bumping

1. Update version in:
   - `setup.py`
   - `pyproject.toml`
   - `CHANGELOG.md`

2. Commit and tag:
   ```bash
   git commit -am "Bump version to X.Y.Z"
   git tag -a vX.Y.Z -m "Release version X.Y.Z"
   git push origin main --tags
   ```

---

## Support

For deployment issues:
- Check [CONTRIBUTING.md](CONTRIBUTING.md)
- Open an issue on GitHub
- Contact: martinlutherupa1@gmail.com

---

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [PyPI Publishing Guide](https://packaging.python.org/tutorials/packaging-projects/)
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)