# API Documentation

## Deutsch-Jozsa Algorithm Module

### Overview

The `deutsch_jozsa` module provides a professional implementation of the Deutsch-Jozsa quantum algorithm using Qiskit. This algorithm demonstrates quantum advantage by determining whether a function is constant or balanced in a single query.

---

## Classes

### `DeutschJozsaAlgorithm`

Main class implementing the Deutsch-Jozsa quantum algorithm.

#### Constructor

```python
DeutschJozsaAlgorithm(n_qubits: int = 3)
```

**Parameters:**
- `n_qubits` (int): Number of input qubits. Must be at least 1. Default is 3.

**Raises:**
- `ValueError`: If `n_qubits` is less than 1.

**Example:**
```python
from deutsch_jozsa import DeutschJozsaAlgorithm

# Create algorithm with 3 qubits
dj = DeutschJozsaAlgorithm(n_qubits=3)
```

---

#### Methods

##### `create_base_circuit()`

Creates the base quantum circuit with initialization.

**Returns:**
- `QuantumCircuit`: Initialized quantum circuit with Hadamard gates applied.

**Example:**
```python
circuit = dj.create_base_circuit()
```

---

##### `create_constant_oracle()`

Creates a constant oracle that returns the same value for all inputs.

**Returns:**
- `QuantumCircuit`: Constant oracle circuit (identity operation).

**Example:**
```python
oracle = dj.create_constant_oracle()
```

---

##### `create_balanced_oracle()`

Creates a balanced oracle that returns 0 for half the inputs and 1 for the other half.

**Returns:**
- `QuantumCircuit`: Balanced oracle circuit with CNOT gates.

**Example:**
```python
oracle = dj.create_balanced_oracle()
```

---

##### `build_circuit(oracle: QuantumCircuit)`

Builds complete Deutsch-Jozsa circuit with the given oracle.

**Parameters:**
- `oracle` (QuantumCircuit): Oracle circuit to insert.

**Returns:**
- `QuantumCircuit`: Complete Deutsch-Jozsa circuit ready for execution.

**Example:**
```python
oracle = dj.create_constant_oracle()
circuit = dj.build_circuit(oracle)
```

---

##### `run_circuit(circuit: QuantumCircuit, shots: int = 1024)`

Executes quantum circuit on simulator.

**Parameters:**
- `circuit` (QuantumCircuit): Circuit to execute.
- `shots` (int): Number of measurement shots. Default is 1024.

**Returns:**
- `Dict[str, int]`: Measurement counts as dictionary.

**Raises:**
- `RuntimeError`: If circuit execution fails.

**Example:**
```python
counts = dj.run_circuit(circuit, shots=2048)
print(counts)  # {'000': 2048}
```

---

##### `interpret_result(counts: Dict[str, int], function_type: str)`

Interprets measurement results to determine function type.

**Parameters:**
- `counts` (Dict[str, int]): Measurement counts from circuit execution.
- `function_type` (str): Expected function type ('constant' or 'balanced').

**Returns:**
- `bool`: True if result matches expected type, False otherwise.

**Raises:**
- `ValueError`: If `function_type` is not 'constant' or 'balanced'.

**Example:**
```python
is_correct = dj.interpret_result(counts, 'constant')
if is_correct:
    print("Function correctly identified as constant")
```

---

##### `visualize_results(counts: Dict[str, int], title: str, save_path: Optional[str] = None)`

Visualizes measurement results as histogram.

**Parameters:**
- `counts` (Dict[str, int]): Measurement counts to visualize.
- `title` (str): Plot title.
- `save_path` (Optional[str]): Path to save figure. If None, only displays.

**Example:**
```python
dj.visualize_results(counts, "Constant Function Results", save_path="results.png")
```

---

##### `run_algorithm(visualize: bool = True)`

Runs complete Deutsch-Jozsa algorithm for both function types.

**Parameters:**
- `visualize` (bool): Whether to display visualizations. Default is True.

**Returns:**
- `Tuple[bool, bool]`: (constant_correct, balanced_correct) indicating test results.

**Example:**
```python
const_correct, balanced_correct = dj.run_algorithm(visualize=True)
print(f"Constant: {const_correct}, Balanced: {balanced_correct}")
```

---

## Functions

### `main()`

Main entry point for command-line execution.

**Example:**
```bash
python deutsch_jozsa.py
```

Or using the installed command:
```bash
deutsch-jozsa
```

---

## Usage Examples

### Basic Usage

```python
from deutsch_jozsa import DeutschJozsaAlgorithm

# Initialize algorithm
dj = DeutschJozsaAlgorithm(n_qubits=3)

# Run complete algorithm
const_correct, balanced_correct = dj.run_algorithm(visualize=True)

print(f"Results: Constant={const_correct}, Balanced={balanced_correct}")
```

### Custom Oracle

```python
from deutsch_jozsa import DeutschJozsaAlgorithm

# Initialize
dj = DeutschJozsaAlgorithm(n_qubits=4)

# Create custom oracle
oracle = dj.create_balanced_oracle()

# Build and run circuit
circuit = dj.build_circuit(oracle)
counts = dj.run_circuit(circuit, shots=2048)

# Interpret results
is_balanced = dj.interpret_result(counts, 'balanced')
print(f"Is balanced: {is_balanced}")
```

### Without Visualization

```python
from deutsch_jozsa import DeutschJozsaAlgorithm

dj = DeutschJozsaAlgorithm(n_qubits=5)
const_correct, balanced_correct = dj.run_algorithm(visualize=False)
```

---

## Error Handling

The module includes comprehensive error handling:

```python
try:
    dj = DeutschJozsaAlgorithm(n_qubits=0)  # Invalid
except ValueError as e:
    print(f"Error: {e}")  # "Number of qubits must be at least 1"

try:
    dj = DeutschJozsaAlgorithm(n_qubits=3)
    counts = {'000': 1024}
    dj.interpret_result(counts, 'invalid')  # Invalid type
except ValueError as e:
    print(f"Error: {e}")  # "Unknown function type: invalid"
```

---

## Logging

The module uses Python's logging module for detailed execution tracking:

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

dj = DeutschJozsaAlgorithm(n_qubits=3)
dj.run_algorithm()  # Will output detailed logs
```

---

## Type Hints

All functions include comprehensive type hints for better IDE support and type checking:

```python
from typing import Dict, Tuple, Optional
from qiskit import QuantumCircuit

def run_circuit(
    self, 
    circuit: QuantumCircuit, 
    shots: int = 1024
) -> Dict[str, int]:
    ...
```

---

## Performance Considerations

- **Qubit Count**: Execution time increases with number of qubits
- **Shots**: More shots provide better statistical accuracy but take longer
- **Visualization**: Disable visualization for faster execution in production

**Recommended Settings:**
- Development: 3-5 qubits, 1024 shots, visualization enabled
- Production: Any qubit count, 1024+ shots, visualization disabled
- Testing: 2-3 qubits, 100 shots, visualization disabled

---

## Version History

- **1.0.0**: Initial release with complete implementation

---

## See Also

- [README.md](../README.md) - Project overview and installation
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines
- [CHANGELOG.md](../CHANGELOG.md) - Version history