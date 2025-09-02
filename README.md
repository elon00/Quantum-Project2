# Deutsch-Jozsa Algorithm Implementation

This project implements the Deutsch-Jozsa quantum algorithm using Qiskit, demonstrating quantum-classical speedup for function classification.

## Algorithm Overview

The Deutsch-Jozsa algorithm determines whether a black-box function is:
- **Constant**: Returns the same value (0 or 1) for all inputs
- **Balanced**: Returns 0 for half the inputs and 1 for the other half

It achieves this in a single quantum measurement, providing exponential speedup over classical approaches.

## Features

- Complete implementation of the Deutsch-Jozsa algorithm
- Support for both constant and balanced oracles
- Quantum circuit simulation using Qiskit Aer
- Result visualization with histograms
- Clear interpretation of measurement outcomes

## Requirements

- Python 3.8+
- Qiskit 2.x
- qiskit-aer
- matplotlib

## Installation

```bash
pip install qiskit qiskit-aer matplotlib
```

## Usage

Run the algorithm:

```bash
python deutsch_jozsa.py
```

The program will:
1. Create quantum circuits for constant and balanced functions
2. Simulate both scenarios
3. Display measurement results
4. Interpret whether each function is constant or balanced

## Expected Output

- **Constant function**: All measurements show '000' (for n=3 qubits)
- **Balanced function**: Measurements show patterns other than '000'

## Code Structure

- `deutsch_jozsa.py`: Main implementation with circuit construction, simulation, and result analysis

## Learning Outcomes

This implementation demonstrates:
- Quantum circuit construction
- Oracle function implementation
- Quantum measurement and interpretation
- Quantum advantage in algorithmic complexity

## References

- Qiskit Documentation
- IBM Quantum Experience
- Quantum Computing textbooks

## License

This project is open-source and available under the MIT License.