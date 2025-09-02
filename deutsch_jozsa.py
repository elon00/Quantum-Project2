from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Number of input qubits
n_qubits = 3

# Step 1: Circuit Initialization
# Create a quantum circuit with n input qubits and 1 output qubit
dj_circuit = QuantumCircuit(n_qubits + 1, n_qubits)

# Initialize the output qubit to |1>
dj_circuit.x(n_qubits)

# Apply Hadamard gates to all qubits (input + output)
dj_circuit.h(range(n_qubits + 1))

# Step 2: Create Oracles

# Constant Oracle: Does nothing (function always returns 0)
oracle_const = QuantumCircuit(n_qubits + 1)
# No gates added for constant function

# Balanced Oracle: CNOT gates from each input qubit to the output qubit
oracle_balanced = QuantumCircuit(n_qubits + 1)
for i in range(n_qubits):
    oracle_balanced.cx(i, n_qubits)

# Step 3: Build Full Circuits

# Constant Function Circuit
dj_const = dj_circuit.copy()
dj_const.compose(oracle_const, inplace=True)
dj_const.barrier()

# Apply final Hadamard gates to input qubits
dj_const.h(range(n_qubits))

# Measure the input qubits
dj_const.measure(range(n_qubits), range(n_qubits))

# Balanced Function Circuit
dj_balanced = dj_circuit.copy()
dj_balanced.compose(oracle_balanced, inplace=True)
dj_balanced.barrier()

# Apply final Hadamard gates to input qubits
dj_balanced.h(range(n_qubits))

# Measure the input qubits
dj_balanced.measure(range(n_qubits), range(n_qubits))

# Step 4: Simulate and Interpret Results

# Use AerSimulator
backend = AerSimulator()

# Simulate constant function
transpiled_const = transpile(dj_const, backend)
job_const = backend.run(transpiled_const, shots=1024)
result_const = job_const.result()
counts_const = result_const.get_counts()

# Simulate balanced function
transpiled_balanced = transpile(dj_balanced, backend)
job_balanced = backend.run(transpiled_balanced, shots=1024)
result_balanced = job_balanced.result()
counts_balanced = result_balanced.get_counts()

# Print results
print("Deutsch-Jozsa Algorithm Results:")
print("Constant function measurement counts:", counts_const)
print("Balanced function measurement counts:", counts_balanced)

# Interpretation
if '000' in counts_const and len(counts_const) == 1:
    print("Constant function: All measurements are 000, confirming it's constant.")
else:
    print("Unexpected result for constant function.")

if '000' not in counts_balanced or len(counts_balanced) > 1:
    print("Balanced function: Measurements are not all 000, confirming it's balanced.")
else:
    print("Unexpected result for balanced function.")

# Visualize results
plot_histogram(counts_const)
plt.title("Constant Function Measurement Results")
plt.show()

plot_histogram(counts_balanced)
plt.title("Balanced Function Measurement Results")
plt.show()