# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Support for custom oracle functions
- Real quantum hardware execution
- Interactive Jupyter notebooks
- Performance benchmarking suite
- Additional quantum algorithms
- Web-based visualization interface

## [1.0.0] - 2025-01-04

### Added
- Initial release of Deutsch-Jozsa Algorithm implementation
- Complete quantum circuit implementation with Qiskit
- Support for constant and balanced oracles
- Professional code structure with classes and type hints
- Comprehensive logging system
- Result visualization with matplotlib
- Detailed docstrings and inline documentation
- Unit tests with pytest
- Integration tests
- CI/CD pipeline with GitHub Actions
- Code quality checks (Black, Flake8, Pylint, mypy)
- Security scanning with Bandit
- Pre-commit hooks configuration
- Professional README with badges and documentation
- MIT License
- Contributing guidelines
- Code of Conduct
- Development requirements file
- Comprehensive .gitignore for Python projects

### Features
- **DeutschJozsaAlgorithm Class**: Object-oriented implementation
  - Configurable number of qubits
  - Separate methods for circuit creation, oracle generation, and execution
  - Built-in result interpretation
  - Visualization capabilities
  
- **Oracle Support**:
  - Constant oracle (returns same value for all inputs)
  - Balanced oracle (returns 0 for half inputs, 1 for other half)
  
- **Testing**:
  - Automated testing with pytest
  - Code coverage reporting
  - Continuous integration
  
- **Documentation**:
  - Comprehensive README
  - API documentation
  - Usage examples
  - Contributing guidelines

### Technical Details
- Python 3.8+ support
- Qiskit 1.0+ compatibility
- Type hints throughout codebase
- Google-style docstrings
- Error handling and logging
- Modular and extensible design

## [0.1.0] - 2024-12-15

### Added
- Basic Deutsch-Jozsa algorithm implementation
- Simple constant and balanced function tests
- Basic visualization
- Initial README

### Changed
- N/A (Initial version)

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- N/A

### Security
- N/A

---

## Version History Summary

- **1.0.0** (2025-01-04): Professional release with complete features, testing, and documentation
- **0.1.0** (2024-12-15): Initial basic implementation

## Migration Guides

### Migrating from 0.1.0 to 1.0.0

The 1.0.0 release introduces a class-based architecture. Here's how to migrate:

**Old code (0.1.0):**
```python
# Direct script execution
python deutsch_jozsa.py
```

**New code (1.0.0):**
```python
from deutsch_jozsa import DeutschJozsaAlgorithm

# Initialize with desired qubits
dj = DeutschJozsaAlgorithm(n_qubits=3)

# Run algorithm
const_correct, balanced_correct = dj.run_algorithm(visualize=True)
```

**Benefits of migration:**
- Better code organization
- Reusable components
- Easier testing
- More flexibility
- Professional error handling

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.

## Links

- [Repository](https://github.com/elon00/Quantum-Project2)
- [Issues](https://github.com/elon00/Quantum-Project2/issues)
- [Pull Requests](https://github.com/elon00/Quantum-Project2/pulls)
- [Releases](https://github.com/elon00/Quantum-Project2/releases)

---

**Note**: This changelog follows the [Keep a Changelog](https://keepachangelog.com/) format and uses [Semantic Versioning](https://semver.org/).