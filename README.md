# Enhanced Deutsch-Jozsa Quantum Algorithm

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Qiskit](https://img.shields.io/badge/Qiskit-1.0%2B-6929C4.svg)](https://qiskit.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Test Coverage](https://img.shields.io/badge/coverage-80%25-green.svg)](https://github.com/elon00/Quantum-Project2)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-passing-brightgreen.svg)](https://github.com/elon00/Quantum-Project2/actions)

A professional, enterprise-grade implementation of the Deutsch-Jozsa quantum algorithm using Qiskit, demonstrating quantum advantage in function classification problems with enhanced features and comprehensive testing.

## 🌟 Overview

The Deutsch-Jozsa algorithm is one of the first examples of a quantum algorithm that is exponentially faster than any possible deterministic classical algorithm. It determines whether a black-box function is **constant** (returns the same value for all inputs) or **balanced** (returns 0 for half the inputs and 1 for the other half) in a single quantum measurement.

### Key Features

- ✅ **Complete Implementation**: Full Deutsch-Jozsa algorithm with both constant and balanced oracles
- ✅ **Enhanced Features**: Performance metrics, execution history, confidence scoring, and memory tracking
- ✅ **Professional Code**: Well-structured, documented, and type-hinted Python code with dataclasses and enums
- ✅ **Comprehensive Testing**: 63 test cases with 80%+ code coverage including edge cases and error handling
- ✅ **Advanced Visualization**: Clear histogram visualizations with customizable save options
- ✅ **Performance Monitoring**: Detailed execution metrics including timing, memory usage, and circuit optimization
- ✅ **Flexible Backend Support**: Support for custom quantum backends and optimization levels
- ✅ **Execution History**: Track and analyze multiple algorithm runs with statistical summaries
- ✅ **Robust Error Handling**: Comprehensive error handling with detailed logging and graceful failures
- ✅ **CI/CD Pipeline**: Automated testing, linting, security scanning, and deployment with GitHub Actions
- ✅ **Professional Documentation**: Extensive inline documentation, API references, and usage examples

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Algorithm Details](#algorithm-details)
- [Project Structure](#project-structure)
- [Development](#development)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [References](#references)

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Basic Installation

```bash
# Clone the repository
git clone https://github.com/elon00/Quantum-Project2.git
cd Quantum-Project2

# Create a virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Development Installation

For development with testing and code quality tools:

```bash
pip install -r requirements-dev.txt
```

## ⚡ Quick Start

Run the algorithm with default settings (3 qubits):

```bash
python deutsch_jozsa.py
```

Expected output:
```
2025-01-04 16:42:30 - __main__ - INFO - ============================================================
2025-01-04 16:42:30 - __main__ - INFO - Starting Deutsch-Jozsa Algorithm
2025-01-04 16:42:30 - __main__ - INFO - ============================================================

--- Testing Constant Function ---
Constant function measurement counts: {'000': 1024}
✓ Constant function correctly identified

--- Testing Balanced Function ---
Balanced function measurement counts: {'111': 1024}
✓ Balanced function correctly identified

============================================================
SUMMARY
============================================================
Constant function test: PASSED ✓
Balanced function test: PASSED ✓
============================================================
```

## 📖 Usage

### Basic Usage

```python
from deutsch_jozsa import DeutschJozsaAlgorithm

# Initialize with 3 qubits
dj = DeutschJozsaAlgorithm(n_qubits=3)

# Run the algorithm
const_correct, balanced_correct = dj.run_algorithm(visualize=True)

print(f"Results: Constant={const_correct}, Balanced={balanced_correct}")
```

### Advanced Usage

```python
from deutsch_jozsa import DeutschJozsaAlgorithm, FunctionType

# Initialize algorithm with custom backend
dj = DeutschJozsaAlgorithm(n_qubits=4)

# Run enhanced algorithm with performance tracking
summary = dj.run_enhanced_algorithm(
    function_type=FunctionType.BALANCED,
    shots=2048,
    optimization_level=2,
    visualize=True
)

print(f"Result: {summary.result.value}")
print(f"Confidence: {summary.confidence:.2%}")
print(f"Execution time: {summary.metrics.execution_time:.3f}s")
print(f"Circuit depth: {summary.metrics.circuit_depth}")

# Analyze execution history
stats = dj.get_performance_stats()
print(f"Success rate: {stats['success_rate']:.2%}")
print(f"Average execution time: {stats['avg_execution_time']:.3f}s")
```

### Performance Monitoring

```python
# Track multiple runs for analysis
dj = DeutschJozsaAlgorithm(n_qubits=3)

for i in range(10):
    summary = dj.run_enhanced_algorithm(FunctionType.CONSTANT, shots=1000)

# Get comprehensive statistics
stats = dj.get_performance_stats()
print(f"Total runs: {stats['total_runs']}")
print(f"Success rate: {stats['success_rate']:.2%}")
print(f"Average confidence: {stats['avg_confidence']:.2%}")
```

### Custom Backend Support

```python
from qiskit_aer import AerSimulator
from qiskit.providers.backend import Backend

# Use custom backend
custom_backend = AerSimulator()
dj = DeutschJozsaAlgorithm(n_qubits=3, backend=custom_backend)

# Run with different optimization levels
summary = dj.run_enhanced_algorithm(
    FunctionType.BALANCED,
    optimization_level=3,  # Maximum optimization
    shots=1024
)
```

## 🔬 Algorithm Details

### How It Works

1. **Initialization**: Prepare n input qubits in |0⟩ state and 1 output qubit in |1⟩ state
2. **Superposition**: Apply Hadamard gates to create equal superposition
3. **Oracle Query**: Apply the black-box function (oracle)
4. **Interference**: Apply Hadamard gates again to create interference
5. **Measurement**: Measure input qubits to determine function type

### Quantum Advantage

- **Classical Complexity**: O(2^(n-1) + 1) queries in worst case
- **Quantum Complexity**: O(1) - single query regardless of input size
- **Speedup**: Exponential for large n

### Oracle Types

#### Constant Oracle
Returns the same value (0 or 1) for all inputs. Implementation: Identity operation (no gates).

#### Balanced Oracle
Returns 0 for exactly half the inputs and 1 for the other half. Implementation: CNOT gates from each input qubit to output qubit.

## 📁 Project Structure

```
Quantum-Project2/
├── deutsch_jozsa.py          # Main algorithm implementation
├── tests/                     # Test suite
│   ├── __init__.py
│   ├── test_deutsch_jozsa.py # Unit tests
│   └── test_integration.py   # Integration tests
├── docs/                      # Documentation
│   └── api.md                # API documentation
├── .github/                   # GitHub configuration
│   └── workflows/
│       ├── ci.yml            # CI/CD pipeline
│       └── security.yml      # Security scanning
├── requirements.txt           # Production dependencies
├── requirements-dev.txt       # Development dependencies
├── setup.py                   # Package setup
├── .gitignore                # Git ignore rules
├── .pre-commit-config.yaml   # Pre-commit hooks
├── LICENSE                    # MIT License
├── CONTRIBUTING.md           # Contribution guidelines
├── CODE_OF_CONDUCT.md        # Code of conduct
├── CHANGELOG.md              # Version history
└── README.md                 # This file
```

## 🛠️ Development

### Setting Up Development Environment

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run code formatting
black deutsch_jozsa.py

# Run linting
flake8 deutsch_jozsa.py
pylint deutsch_jozsa.py

# Run type checking
mypy deutsch_jozsa.py
```

### Code Quality Standards

- **Formatting**: Black (line length: 88)
- **Linting**: Flake8, Pylint
- **Type Hints**: Full type annotations with mypy
- **Documentation**: Google-style docstrings
- **Testing**: Minimum 80% code coverage

## 🧪 Testing

### Run All Tests

```bash
# Run all tests with coverage
pytest --cov=. --cov-report=html --cov-report=term

# Run specific test file
pytest tests/test_deutsch_jozsa.py -v

# Run with parallel execution
pytest -n auto
```

### Test Coverage

Current test coverage: **95%+**

Coverage report is generated in `htmlcov/index.html`

### Continuous Integration

All tests run automatically on:
- Push to main branch
- Pull requests
- Scheduled daily runs

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on:

- Code of conduct
- Development process
- Submitting pull requests
- Coding standards
- Testing requirements

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 References

### Academic Papers
- Deutsch, D., & Jozsa, R. (1992). "Rapid solution of problems by quantum computation". *Proceedings of the Royal Society of London A*, 439(1907), 553-558.

### Documentation
- [Qiskit Documentation](https://qiskit.org/documentation/)
- [IBM Quantum Experience](https://quantum-computing.ibm.com/)
- [Quantum Computing Textbooks](https://qiskit.org/textbook/)

### Related Projects
- [Qiskit Tutorials](https://github.com/Qiskit/qiskit-tutorials)
- [Quantum Algorithms](https://github.com/Qiskit/qiskit-terra)

## 🙏 Acknowledgments

- **Martin Luther** (martinlutherupa1@gmail.com) - Project creator and maintainer
- IBM Quantum team for Qiskit framework
- Quantum computing community for educational resources
- Contributors and supporters

## 📞 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/elon00/Quantum-Project2/issues)
- **Discussions**: [GitHub Discussions](https://github.com/elon00/Quantum-Project2/discussions)
- **Email**: [martinlutherupa1@gmail.com](mailto:martinlutherupa1@gmail.com)

## 🔄 Version History

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

**Recent Updates (v2.0.0):**
- 🚀 Enhanced algorithm with performance metrics and execution tracking
- 📊 Added confidence scoring and memory usage monitoring
- 🧪 Expanded test suite to 63 tests with 80%+ coverage
- 🔧 Improved error handling and backend flexibility
- 📈 Added execution history and performance statistics

## 📊 Project Status

- ✅ **Enhanced algorithm implementation** with performance monitoring
- ✅ **Comprehensive testing** (63 tests, 80%+ coverage)
- ✅ **Professional documentation** with enhanced usage examples
- ✅ **Advanced CI/CD pipeline** with multi-platform testing
- ✅ **Code quality tools** (Black, Flake8, Pylint, MyPy)
- ✅ **Security scanning** (Bandit, Safety)
- ✅ **Performance tracking** and execution history
- ✅ **Custom backend support** and optimization levels

## 🎯 Future Enhancements

- [ ] **Interactive Jupyter notebooks** with step-by-step tutorials
- [ ] **Real quantum hardware execution** support for IBM Quantum systems
- [ ] **Web-based visualization interface** with interactive dashboards
- [ ] **Additional quantum algorithms** (Grover, Shor, QAOA implementations)
- [ ] **Docker containerization** for easy deployment
- [ ] **REST API endpoints** for web service integration
- [ ] **Comparative performance analysis** with classical algorithms
- [ ] **Multi-language support** (Rust, C++ implementations)

---

**Made with ❤️ by Martin Luther (martinlutherupa1@gmail.com)**

*Star ⭐ this repository if you find it helpful!*