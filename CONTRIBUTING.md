# Contributing to Deutsch-Jozsa Quantum Algorithm

First off, thank you for considering contributing to this project! It's people like you that make this quantum computing implementation better for everyone.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Process](#development-process)
- [Style Guidelines](#style-guidelines)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)
- [Testing Guidelines](#testing-guidelines)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic understanding of quantum computing concepts
- Familiarity with Qiskit

### Setting Up Your Development Environment

1. **Fork the repository** on GitHub

2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Quantum-Project2.git
   cd Quantum-Project2
   ```

3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install development dependencies**:
   ```bash
   pip install -r requirements-dev.txt
   ```

5. **Install pre-commit hooks**:
   ```bash
   pre-commit install
   ```

6. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected behavior** vs actual behavior
- **Environment details** (OS, Python version, Qiskit version)
- **Code samples** or error messages
- **Screenshots** if applicable

Use the bug report template when available.

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear title and description**
- **Use case** and motivation
- **Proposed solution** or implementation approach
- **Alternative solutions** considered
- **Additional context** or examples

### Your First Code Contribution

Unsure where to begin? Look for issues labeled:

- `good first issue` - Simple issues for newcomers
- `help wanted` - Issues where we need community help
- `documentation` - Documentation improvements

### Pull Requests

We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`
2. Make your changes following our style guidelines
3. Add tests for any new functionality
4. Ensure all tests pass
5. Update documentation as needed
6. Submit your pull request

## Development Process

### Workflow

1. **Create an issue** first to discuss major changes
2. **Write code** following our style guidelines
3. **Add tests** to maintain coverage above 80%
4. **Update documentation** for any API changes
5. **Run tests** locally before pushing
6. **Submit PR** with clear description

### Branch Naming Convention

- `feature/` - New features
- `bugfix/` - Bug fixes
- `hotfix/` - Urgent fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions or modifications

Examples:
- `feature/add-custom-oracle`
- `bugfix/fix-measurement-error`
- `docs/update-api-reference`

## Style Guidelines

### Python Code Style

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with some modifications:

- **Line length**: 88 characters (Black default)
- **Indentation**: 4 spaces
- **Quotes**: Double quotes for strings
- **Imports**: Organized with isort

### Code Formatting

We use automated tools for consistency:

```bash
# Format code with Black
black deutsch_jozsa.py

# Sort imports with isort
isort deutsch_jozsa.py

# Check style with flake8
flake8 deutsch_jozsa.py

# Type check with mypy
mypy deutsch_jozsa.py

# Lint with pylint
pylint deutsch_jozsa.py
```

### Documentation Style

- Use **Google-style docstrings**
- Include type hints for all functions
- Document all public APIs
- Add examples for complex functionality

Example:
```python
def function_name(param1: int, param2: str) -> bool:
    """
    Brief description of function.
    
    Longer description if needed, explaining the purpose
    and behavior in detail.
    
    Args:
        param1 (int): Description of param1
        param2 (str): Description of param2
        
    Returns:
        bool: Description of return value
        
    Raises:
        ValueError: When param1 is negative
        
    Example:
        >>> result = function_name(5, "test")
        >>> print(result)
        True
    """
    pass
```

## Commit Messages

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements

### Examples

```
feat(oracle): add support for custom oracle functions

Implement functionality to allow users to define custom
oracle functions for the Deutsch-Jozsa algorithm.

Closes #123
```

```
fix(measurement): correct qubit measurement order

The measurement was reading qubits in reverse order,
causing incorrect results for balanced functions.

Fixes #456
```

### Guidelines

- Use present tense ("add feature" not "added feature")
- Use imperative mood ("move cursor to..." not "moves cursor to...")
- Limit first line to 72 characters
- Reference issues and pull requests in footer

## Pull Request Process

### Before Submitting

1. **Update documentation** for any changed functionality
2. **Add tests** for new features
3. **Run full test suite**: `pytest --cov=.`
4. **Check code quality**: `flake8 . && pylint deutsch_jozsa.py`
5. **Format code**: `black . && isort .`
6. **Update CHANGELOG.md** with your changes

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe testing performed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] No new warnings
```

### Review Process

1. **Automated checks** must pass (CI/CD)
2. **Code review** by at least one maintainer
3. **Address feedback** and update PR
4. **Approval** from maintainer
5. **Merge** by maintainer

## Testing Guidelines

### Writing Tests

- Use `pytest` framework
- Aim for >80% code coverage
- Test edge cases and error conditions
- Use descriptive test names

Example:
```python
def test_constant_oracle_returns_all_zeros():
    """Test that constant oracle produces all-zero measurements."""
    dj = DeutschJozsaAlgorithm(n_qubits=3)
    oracle = dj.create_constant_oracle()
    circuit = dj.build_circuit(oracle)
    counts = dj.run_circuit(circuit)
    
    assert '000' in counts
    assert len(counts) == 1
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_deutsch_jozsa.py

# Run specific test
pytest tests/test_deutsch_jozsa.py::test_constant_oracle

# Run in parallel
pytest -n auto
```

### Test Organization

```
tests/
├── __init__.py
├── test_deutsch_jozsa.py      # Unit tests
├── test_integration.py         # Integration tests
├── test_performance.py         # Performance tests
└── conftest.py                 # Shared fixtures
```

## Additional Resources

### Learning Resources

- [Qiskit Documentation](https://qiskit.org/documentation/)
- [Quantum Computing Basics](https://qiskit.org/textbook/)
- [Python Best Practices](https://docs.python-guide.org/)

### Communication

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and general discussion
- **Pull Requests**: Code contributions

## Recognition

Contributors will be recognized in:
- README.md contributors section
- CHANGELOG.md for significant contributions
- GitHub contributors page

## Questions?

Don't hesitate to ask questions by:
- Opening a GitHub issue
- Starting a GitHub discussion
- Reaching out to maintainers

Thank you for contributing! 🎉