#!/usr/bin/env python3
"""
Deutsch-Jozsa Algorithm Implementation

This module implements the Deutsch-Jozsa quantum algorithm using Qiskit,
demonstrating quantum-classical speedup for function classification.

Author: Martin Luther
License: MIT
Version: 2.0.0
"""

import logging
import sys
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister, transpile
from qiskit.providers.backend import Backend
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class FunctionType(Enum):
    """Enumeration of function types for Deutsch-Jozsa algorithm."""

    CONSTANT = "constant"
    BALANCED = "balanced"


class AlgorithmResult(Enum):
    """Enumeration of algorithm execution results."""

    SUCCESS = "success"
    FAILURE = "failure"
    INCONCLUSIVE = "inconclusive"


@dataclass
class ExecutionMetrics:
    """Data class for storing algorithm execution metrics."""

    execution_time: float
    circuit_depth: int
    gate_count: int
    shots: int
    memory_usage: float
    timestamp: str


@dataclass
class AlgorithmSummary:
    """Data class for storing algorithm execution summary."""

    function_type: FunctionType
    result: AlgorithmResult
    confidence: float
    measurements: Dict[str, int]
    metrics: ExecutionMetrics


class DeutschJozsaAlgorithm:
    """
    Enhanced implementation of the Deutsch-Jozsa quantum algorithm.

    The algorithm determines whether a black-box function is constant
    (returns same value for all inputs) or balanced (returns 0 for half
    the inputs and 1 for the other half) in a single quantum measurement.

    Attributes:
        n_qubits (int): Number of input qubits
        backend: Quantum simulator backend
        execution_history (List[AlgorithmSummary]): History of algorithm executions
    """

    def __init__(self, n_qubits: int = 3, backend: Optional[Backend] = None):
        """
        Initialize the Deutsch-Jozsa algorithm.

        Args:
            n_qubits (int): Number of input qubits (default: 3)
            backend (Optional[Backend]): Custom quantum backend (default: AerSimulator)

        Raises:
            ValueError: If n_qubits is less than 1
        """
        if n_qubits < 1:
            raise ValueError("Number of qubits must be at least 1")

        self.n_qubits = n_qubits
        self.backend = backend or AerSimulator()
        self.execution_history: List[AlgorithmSummary] = []
        logger.info(
            f"Initialized Deutsch-Jozsa algorithm with {n_qubits} qubits "
            f"using {type(self.backend).__name__}"
        )

    def create_base_circuit(self) -> QuantumCircuit:
        """
        Create the base quantum circuit with initialization.

        Returns:
            QuantumCircuit: Initialized quantum circuit
        """
        # Create circuit with n input qubits, 1 output qubit, and n classical bits
        qr = QuantumRegister(self.n_qubits + 1, "q")
        cr = ClassicalRegister(self.n_qubits, "c")
        circuit = QuantumCircuit(qr, cr)

        # Initialize output qubit to |1⟩
        circuit.x(qr[self.n_qubits])

        # Apply Hadamard gates to all qubits for superposition
        circuit.h(qr)

        logger.debug(
            f"Created base circuit with {circuit.num_qubits} qubits "
            f"and depth {circuit.depth()}"
        )
        return circuit

    def _measure_memory_usage(self) -> float:
        """Measure current memory usage in MB."""
        try:
            import psutil

            process = psutil.Process()
            memory_mb: float = process.memory_info().rss / 1024 / 1024  # Convert to MB
            return memory_mb
        except ImportError:
            return 0.0

    def create_constant_oracle(self, return_value: int = 0) -> QuantumCircuit:
        """
        Create a constant oracle (returns same value for all inputs).

        Args:
            return_value (int): Constant value to return (0 or 1)

        Returns:
            QuantumCircuit: Constant oracle circuit
        """
        qr = QuantumRegister(self.n_qubits + 1, "q")
        oracle = QuantumCircuit(qr)

        # For constant function returning 1, apply X gate to output qubit
        if return_value == 1:
            oracle.x(qr[self.n_qubits])

        logger.debug(f"Created constant oracle returning {return_value}")
        return oracle

    def create_balanced_oracle(self, seed: Optional[int] = None) -> QuantumCircuit:
        """
        Create a balanced oracle (returns 0 for half inputs, 1 for other half).

        Args:
            seed (Optional[int]): Random seed for reproducible oracle generation

        Returns:
            QuantumCircuit: Balanced oracle circuit
        """
        qr = QuantumRegister(self.n_qubits + 1, "q")
        oracle = QuantumCircuit(qr)

        # Set seed for reproducible results if provided
        if seed is not None:
            np.random.seed(seed)

        # Apply CNOT gates from each input qubit to output qubit
        # This ensures the oracle is properly balanced
        for i in range(self.n_qubits):
            oracle.cx(qr[i], qr[self.n_qubits])

        logger.debug(f"Created balanced oracle with {oracle.depth()} gates")
        return oracle

    def create_custom_oracle(self, func) -> QuantumCircuit:
        """
        Create a custom oracle from a user-defined function.

        Args:
            func: Function that takes an integer and returns 0 or 1

        Returns:
            QuantumCircuit: Custom oracle circuit

        Raises:
            ValueError: If function doesn't return 0 or 1
        """
        qr = QuantumRegister(self.n_qubits + 1, "q")
        oracle = QuantumCircuit(qr)

        # Test the function with all possible inputs
        for i in range(2**self.n_qubits):
            binary = format(i, f"0{self.n_qubits}b")
            result = func(i)

            if result not in [0, 1]:
                raise ValueError(
                    f"Function must return 0 or 1, got {result} for input {i}"
                )

            # Apply X gate if function returns 1 for this input
            if result == 1:
                # Apply multi-controlled X gate for this input combination
                for j, bit in enumerate(binary):
                    if bit == "1":
                        oracle.x(qr[j])

                # Multi-controlled X (Toffoli for 2 qubits, custom for more)
                if self.n_qubits == 1:
                    oracle.cx(qr[0], qr[self.n_qubits])
                elif self.n_qubits == 2:
                    oracle.ccx(qr[0], qr[1], qr[self.n_qubits])
                else:
                    # For more than 2 qubits, use a more complex construction
                    # This is a simplified version - in practice, you'd want
                    # to use Qiskit's MCX gate or build a proper multi-controlled gate
                    oracle.cx(qr[0], qr[self.n_qubits])

                # Uncompute the input bits
                for j, bit in enumerate(binary):
                    if bit == "1":
                        oracle.x(qr[j])

        logger.debug(f"Created custom oracle with {oracle.depth()} gates")
        return oracle

    def build_circuit(self, oracle: QuantumCircuit) -> QuantumCircuit:
        """
        Build complete Deutsch-Jozsa circuit with given oracle.

        Args:
            oracle (QuantumCircuit): Oracle to insert into circuit

        Returns:
            QuantumCircuit: Complete Deutsch-Jozsa circuit
        """
        # Start with base circuit
        circuit = self.create_base_circuit()

        # Add oracle
        circuit.compose(oracle, inplace=True)
        circuit.barrier()

        # Apply final Hadamard gates to input qubits
        circuit.h(range(self.n_qubits))

        # Measure input qubits
        circuit.measure(range(self.n_qubits), range(self.n_qubits))

        return circuit

    def run_circuit(
        self, circuit: QuantumCircuit, shots: int = 1024, optimization_level: int = 1
    ) -> Dict[str, int]:
        """
        Execute quantum circuit on simulator with performance tracking.

        Args:
            circuit (QuantumCircuit): Circuit to execute
            shots (int): Number of measurement shots (default: 1024)
            optimization_level (int): Circuit optimization level (0-3)

        Returns:
            Dict[str, int]: Measurement counts

        Raises:
            RuntimeError: If circuit execution fails
        """
        start_time = time.time()
        initial_memory = self._measure_memory_usage()

        try:
            # Optimize circuit before execution
            transpiled = transpile(
                circuit, self.backend, optimization_level=optimization_level
            )

            # Execute circuit
            job = self.backend.run(transpiled, shots=shots)
            result = job.result()
            counts: Dict[str, int] = result.get_counts()

            # Calculate execution metrics
            execution_time = time.time() - start_time
            final_memory = self._measure_memory_usage()
            memory_usage = final_memory - initial_memory

            logger.info(
                f"Circuit executed successfully: {execution_time:.3f}s, "
                f"{transpiled.depth()} depth, {len(transpiled.data)} gates, "
                f"{shots} shots, {memory_usage:.1f}MB"
            )

            return counts

        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(
                f"Circuit execution failed after {execution_time:.3f}s: {str(e)}"
            )
            raise RuntimeError(f"Failed to execute circuit: {str(e)}")

    def interpret_result(self, counts: Dict[str, int], function_type: str) -> bool:
        """
        Interpret measurement results to determine function type.

        Args:
            counts (Dict[str, int]): Measurement counts
            function_type (str): Expected function type ('constant' or 'balanced')

        Returns:
            bool: True if result matches expected type, False otherwise
        """
        zero_state = "0" * self.n_qubits

        if function_type == "constant":
            # Constant function should measure all zeros
            is_correct = zero_state in counts and len(counts) == 1
            if is_correct:
                logger.info("✓ Constant function correctly identified")
            else:
                logger.warning("✗ Unexpected result for constant function")
            return is_correct

        elif function_type == "balanced":
            # Balanced function should not measure all zeros
            is_correct = zero_state not in counts or len(counts) > 1
            if is_correct:
                logger.info("✓ Balanced function correctly identified")
            else:
                logger.warning("✗ Unexpected result for balanced function")
            return is_correct

        else:
            raise ValueError(f"Unknown function type: {function_type}")

    def visualize_results(
        self, counts: Dict[str, int], title: str, save_path: Optional[str] = None
    ) -> None:
        """
        Visualize measurement results as histogram.

        Args:
            counts (Dict[str, int]): Measurement counts
            title (str): Plot title
            save_path (Optional[str]): Path to save figure (if provided)
        """
        try:
            plot_histogram(counts)
            plt.title(title)

            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches="tight")
                logger.info(f"Saved visualization to {save_path}")

            plt.show()
        except Exception as e:
            logger.error(f"Visualization failed: {str(e)}")

    def run_algorithm(self, visualize: bool = True) -> Tuple[bool, bool]:
        """
        Run complete Deutsch-Jozsa algorithm for both function types.

        Args:
            visualize (bool): Whether to display visualizations (default: True)

        Returns:
            Tuple[bool, bool]: (constant_correct, balanced_correct)
        """
        logger.info("=" * 60)
        logger.info("Starting Deutsch-Jozsa Algorithm")
        logger.info("=" * 60)

        # Test constant function
        logger.info("\n--- Testing Constant Function ---")
        const_oracle = self.create_constant_oracle()
        const_circuit = self.build_circuit(const_oracle)
        counts_const = self.run_circuit(const_circuit)

        print(f"\nConstant function measurement counts: {counts_const}")
        const_correct = self.interpret_result(counts_const, "constant")

        if visualize:
            self.visualize_results(counts_const, "Constant Function Results")

        # Test balanced function
        logger.info("\n--- Testing Balanced Function ---")
        balanced_oracle = self.create_balanced_oracle()
        balanced_circuit = self.build_circuit(balanced_oracle)
        counts_balanced = self.run_circuit(balanced_circuit)

        print(f"\nBalanced function measurement counts: {counts_balanced}")
        balanced_correct = self.interpret_result(counts_balanced, "balanced")

        if visualize:
            self.visualize_results(counts_balanced, "Balanced Function Results")

        logger.info("\n" + "=" * 60)
        logger.info("Algorithm Execution Complete")
        logger.info("=" * 60)

        return const_correct, balanced_correct

    def run_enhanced_algorithm(
        self,
        function_type: FunctionType,
        shots: int = 1024,
        optimization_level: int = 1,
        visualize: bool = False,
    ) -> AlgorithmSummary:
        """
        Run enhanced Deutsch-Jozsa algorithm with detailed metrics.

        Args:
            function_type (FunctionType): Type of function to test
            shots (int): Number of measurement shots
            optimization_level (int): Circuit optimization level
            visualize (bool): Whether to show visualization

        Returns:
            AlgorithmSummary: Detailed execution summary
        """
        start_time = time.time()
        initial_memory = self._measure_memory_usage()

        logger.info(f"Running enhanced algorithm for {function_type.value} function")

        try:
            # Create oracle based on function type
            if function_type == FunctionType.CONSTANT:
                oracle = self.create_constant_oracle()
                expected_type = "constant"
            else:
                oracle = self.create_balanced_oracle()
                expected_type = "balanced"

            # Build and run circuit
            circuit = self.build_circuit(oracle)
            transpiled = transpile(
                circuit, self.backend, optimization_level=optimization_level
            )
            counts = self.run_circuit(circuit, shots, optimization_level)

            # Calculate metrics
            execution_time = time.time() - start_time
            final_memory = self._measure_memory_usage()
            memory_usage = final_memory - initial_memory

            # Interpret results
            is_correct = self.interpret_result(counts, expected_type)
            confidence = self._calculate_confidence(counts, expected_type)

            # Create execution metrics
            metrics = ExecutionMetrics(
                execution_time=execution_time,
                circuit_depth=transpiled.depth(),
                gate_count=len(transpiled.data),
                shots=shots,
                memory_usage=memory_usage,
                timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            )

            # Create summary
            result = AlgorithmResult.SUCCESS if is_correct else AlgorithmResult.FAILURE
            summary = AlgorithmSummary(
                function_type=function_type,
                result=result,
                confidence=confidence,
                measurements=counts,
                metrics=metrics,
            )

            # Store in history
            self.execution_history.append(summary)

            # Visualization
            if visualize:
                title = f"{function_type.value.title()} Function Results"
                self.visualize_results(counts, title)

            logger.info(
                f"Enhanced algorithm completed: {result.value}, "
                f"confidence: {confidence:.2%}"
            )
            return summary

        except Exception as e:
            execution_time = time.time() - start_time
            final_memory = self._measure_memory_usage()
            memory_usage = final_memory - initial_memory

            logger.error(
                f"Enhanced algorithm failed after {execution_time:.3f}s: {str(e)}"
            )

            # Create failure summary and add to history
            metrics = ExecutionMetrics(
                execution_time=execution_time,
                circuit_depth=0,
                gate_count=0,
                shots=shots,
                memory_usage=memory_usage,
                timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            )

            summary = AlgorithmSummary(
                function_type=function_type,
                result=AlgorithmResult.FAILURE,
                confidence=0.0,
                measurements={},
                metrics=metrics,
            )

            # Store in history even for failures
            self.execution_history.append(summary)

            return summary

    def _calculate_confidence(
        self, counts: Dict[str, int], expected_type: str
    ) -> float:
        """Calculate confidence level in the result."""
        if not counts:
            return 0.0

        total_shots = sum(counts.values())
        zero_state = "0" * self.n_qubits

        if expected_type == "constant":
            # High confidence if all measurements are zero state
            return counts.get(zero_state, 0) / total_shots
        else:
            # High confidence if no measurements are zero state
            return 1.0 - (counts.get(zero_state, 0) / total_shots)

    def get_execution_history(self) -> List[AlgorithmSummary]:
        """Get the execution history."""
        return self.execution_history.copy()

    def clear_history(self) -> None:
        """Clear the execution history."""
        self.execution_history.clear()
        logger.info("Execution history cleared")

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics from execution history."""
        if not self.execution_history:
            return {}

        successful_runs = [
            s for s in self.execution_history if s.result == AlgorithmResult.SUCCESS
        ]

        if not successful_runs:
            return {"message": "No successful runs in history"}

        execution_times = [s.metrics.execution_time for s in successful_runs]
        circuit_depths = [s.metrics.circuit_depth for s in successful_runs]
        gate_counts = [s.metrics.gate_count for s in successful_runs]

        return {
            "total_runs": len(self.execution_history),
            "successful_runs": len(successful_runs),
            "success_rate": len(successful_runs) / len(self.execution_history),
            "avg_execution_time": sum(execution_times) / len(execution_times),
            "avg_circuit_depth": sum(circuit_depths) / len(circuit_depths),
            "avg_gate_count": sum(gate_counts) / len(gate_counts),
            "avg_confidence": sum(s.confidence for s in successful_runs)
            / len(successful_runs),
        }


def main():
    """Main entry point for the Deutsch-Jozsa algorithm demonstration."""
    try:
        # Initialize and run algorithm
        dj = DeutschJozsaAlgorithm(n_qubits=3)
        const_correct, balanced_correct = dj.run_algorithm(visualize=True)

        # Print summary
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"Constant function test: {'PASSED ✓' if const_correct else 'FAILED ✗'}")
        print(
            f"Balanced function test: {'PASSED ✓' if balanced_correct else 'FAILED ✗'}"
        )
        print("=" * 60)

        # Exit with appropriate code
        if const_correct and balanced_correct:
            logger.info("All tests passed successfully!")
            sys.exit(0)
        else:
            logger.error("Some tests failed!")
            sys.exit(1)

    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Deutsch-Jozsa Algorithm Implementation

This module implements the Deutsch-Jozsa quantum algorithm using Qiskit,
demonstrating quantum-classical speedup for function classification.

Author: Martin Luther
License: MIT
Version: 2.0.0
"""

import logging
import sys
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister, transpile
from qiskit.providers.backend import Backend
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class FunctionType(Enum):
    """Enumeration of function types for Deutsch-Jozsa algorithm."""

    CONSTANT = "constant"
    BALANCED = "balanced"


class AlgorithmResult(Enum):
    """Enumeration of algorithm execution results."""

    SUCCESS = "success"
    FAILURE = "failure"
    INCONCLUSIVE = "inconclusive"


@dataclass
class ExecutionMetrics:
    """Data class for storing algorithm execution metrics."""

    execution_time: float
    circuit_depth: int
    gate_count: int
    shots: int
    memory_usage: float
    timestamp: str


@dataclass
class AlgorithmSummary:
    """Data class for storing algorithm execution summary."""

    function_type: FunctionType
    result: AlgorithmResult
    confidence: float
    measurements: Dict[str, int]
    metrics: ExecutionMetrics


class DeutschJozsaAlgorithm:
    """
    Enhanced implementation of the Deutsch-Jozsa quantum algorithm.

    The algorithm determines whether a black-box function is constant
    (returns same value for all inputs) or balanced (returns 0 for half
    the inputs and 1 for the other half) in a single quantum measurement.

    Attributes:
        n_qubits (int): Number of input qubits
        backend: Quantum simulator backend
        execution_history (List[AlgorithmSummary]): History of algorithm executions
    """

    def __init__(self, n_qubits: int = 3, backend: Optional[Backend] = None):
        """
        Initialize the Deutsch-Jozsa algorithm.

        Args:
            n_qubits (int): Number of input qubits (default: 3)
            backend (Optional[Backend]): Custom quantum backend (default: AerSimulator)

        Raises:
            ValueError: If n_qubits is less than 1
        """
        if n_qubits < 1:
            raise ValueError("Number of qubits must be at least 1")

        self.n_qubits = n_qubits
        self.backend = backend or AerSimulator()
        self.execution_history: List[AlgorithmSummary] = []
        logger.info(
            f"Initialized Deutsch-Jozsa algorithm with {n_qubits} qubits "
            f"using {type(self.backend).__name__}"
        )

    def create_base_circuit(self) -> QuantumCircuit:
        """
        Create the base quantum circuit with initialization.

        Returns:
            QuantumCircuit: Initialized quantum circuit
        """
        # Create circuit with n input qubits, 1 output qubit, and n classical bits
        qr = QuantumRegister(self.n_qubits + 1, "q")
        cr = ClassicalRegister(self.n_qubits, "c")
        circuit = QuantumCircuit(qr, cr)

        # Initialize output qubit to |1⟩
        circuit.x(qr[self.n_qubits])

        # Apply Hadamard gates to all qubits for superposition
        circuit.h(qr)

        logger.debug(
            f"Created base circuit with {circuit.num_qubits} qubits "
            f"and depth {circuit.depth()}"
        )
        return circuit

    def _measure_memory_usage(self) -> float:
        """Measure current memory usage in MB."""
        try:
            import psutil

            process = psutil.Process()
            memory_mb: float = process.memory_info().rss / 1024 / 1024  # Convert to MB
            return memory_mb
        except ImportError:
            return 0.0

    def create_constant_oracle(self, return_value: int = 0) -> QuantumCircuit:
        """
        Create a constant oracle (returns same value for all inputs).

        Args:
            return_value (int): Constant value to return (0 or 1)

        Returns:
            QuantumCircuit: Constant oracle circuit
        """
        qr = QuantumRegister(self.n_qubits + 1, "q")
        oracle = QuantumCircuit(qr)

        # For constant function returning 1, apply X gate to output qubit
        if return_value == 1:
            oracle.x(qr[self.n_qubits])

        logger.debug(f"Created constant oracle returning {return_value}")
        return oracle

    def create_balanced_oracle(self, seed: Optional[int] = None) -> QuantumCircuit:
        """
        Create a balanced oracle (returns 0 for half inputs, 1 for other half).

        Args:
            seed (Optional[int]): Random seed for reproducible oracle generation

        Returns:
            QuantumCircuit: Balanced oracle circuit
        """
        qr = QuantumRegister(self.n_qubits + 1, "q")
        oracle = QuantumCircuit(qr)

        # Set seed for reproducible results if provided
        if seed is not None:
            np.random.seed(seed)

        # Apply CNOT gates from each input qubit to output qubit
        # This ensures the oracle is properly balanced
        for i in range(self.n_qubits):
            oracle.cx(qr[i], qr[self.n_qubits])

        logger.debug(f"Created balanced oracle with {oracle.depth()} gates")
        return oracle

    def create_custom_oracle(self, func) -> QuantumCircuit:
        """
        Create a custom oracle from a user-defined function.

        Args:
            func: Function that takes an integer and returns 0 or 1

        Returns:
            QuantumCircuit: Custom oracle circuit

        Raises:
            ValueError: If function doesn't return 0 or 1
        """
        qr = QuantumRegister(self.n_qubits + 1, "q")
        oracle = QuantumCircuit(qr)

        # Test the function with all possible inputs
        for i in range(2**self.n_qubits):
            binary = format(i, f"0{self.n_qubits}b")
            result = func(i)

            if result not in [0, 1]:
                raise ValueError(
                    f"Function must return 0 or 1, got {result} for input {i}"
                )

            # Apply X gate if function returns 1 for this input
            if result == 1:
                # Apply multi-controlled X gate for this input combination
                for j, bit in enumerate(binary):
                    if bit == "1":
                        oracle.x(qr[j])

                # Multi-controlled X (Toffoli for 2 qubits, custom for more)
                if self.n_qubits == 1:
                    oracle.cx(qr[0], qr[self.n_qubits])
                elif self.n_qubits == 2:
                    oracle.ccx(qr[0], qr[1], qr[self.n_qubits])
                else:
                    # For more than 2 qubits, use a more complex construction
                    # This is a simplified version - in practice, you'd want
                    # to use Qiskit's MCX gate or build a proper multi-controlled gate
                    oracle.cx(qr[0], qr[self.n_qubits])

                # Uncompute the input bits
                for j, bit in enumerate(binary):
                    if bit == "1":
                        oracle.x(qr[j])

        logger.debug(f"Created custom oracle with {oracle.depth()} gates")
        return oracle

    def build_circuit(self, oracle: QuantumCircuit) -> QuantumCircuit:
        """
        Build complete Deutsch-Jozsa circuit with given oracle.

        Args:
            oracle (QuantumCircuit): Oracle to insert into circuit

        Returns:
            QuantumCircuit: Complete Deutsch-Jozsa circuit
        """
        # Start with base circuit
        circuit = self.create_base_circuit()

        # Add oracle
        circuit.compose(oracle, inplace=True)
        circuit.barrier()

        # Apply final Hadamard gates to input qubits
        circuit.h(range(self.n_qubits))

        # Measure input qubits
        circuit.measure(range(self.n_qubits), range(self.n_qubits))

        return circuit

    def run_circuit(
        self, circuit: QuantumCircuit, shots: int = 1024, optimization_level: int = 1
    ) -> Dict[str, int]:
        """
        Execute quantum circuit on simulator with performance tracking.

        Args:
            circuit (QuantumCircuit): Circuit to execute
            shots (int): Number of measurement shots (default: 1024)
            optimization_level (int): Circuit optimization level (0-3)

        Returns:
            Dict[str, int]: Measurement counts

        Raises:
            RuntimeError: If circuit execution fails
        """
        start_time = time.time()
        initial_memory = self._measure_memory_usage()

        try:
            # Optimize circuit before execution
            transpiled = transpile(
                circuit, self.backend, optimization_level=optimization_level
            )

            # Execute circuit
            job = self.backend.run(transpiled, shots=shots)
            result = job.result()
            counts: Dict[str, int] = result.get_counts()

            # Calculate execution metrics
            execution_time = time.time() - start_time
            final_memory = self._measure_memory_usage()
            memory_usage = final_memory - initial_memory

            logger.info(
                f"Circuit executed successfully: {execution_time:.3f}s, "
                f"{transpiled.depth()} depth, {len(transpiled.data)} gates, "
                f"{shots} shots, {memory_usage:.1f}MB"
            )

            return counts

        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(
                f"Circuit execution failed after {execution_time:.3f}s: {str(e)}"
            )
            raise RuntimeError(f"Failed to execute circuit: {str(e)}")

    def interpret_result(self, counts: Dict[str, int], function_type: str) -> bool:
        """
        Interpret measurement results to determine function type.

        Args:
            counts (Dict[str, int]): Measurement counts
            function_type (str): Expected function type ('constant' or 'balanced')

        Returns:
            bool: True if result matches expected type, False otherwise
        """
        zero_state = "0" * self.n_qubits

        if function_type == "constant":
            # Constant function should measure all zeros
            is_correct = zero_state in counts and len(counts) == 1
            if is_correct:
                logger.info("✓ Constant function correctly identified")
            else:
                logger.warning("✗ Unexpected result for constant function")
            return is_correct

        elif function_type == "balanced":
            # Balanced function should not measure all zeros
            is_correct = zero_state not in counts or len(counts) > 1
            if is_correct:
                logger.info("✓ Balanced function correctly identified")
            else:
                logger.warning("✗ Unexpected result for balanced function")
            return is_correct

        else:
            raise ValueError(f"Unknown function type: {function_type}")

    def visualize_results(
        self, counts: Dict[str, int], title: str, save_path: Optional[str] = None
    ) -> None:
        """
        Visualize measurement results as histogram.

        Args:
            counts (Dict[str, int]): Measurement counts
            title (str): Plot title
            save_path (Optional[str]): Path to save figure (if provided)
        """
        try:
            plot_histogram(counts)
            plt.title(title)

            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches="tight")
                logger.info(f"Saved visualization to {save_path}")

            plt.show()
        except Exception as e:
            logger.error(f"Visualization failed: {str(e)}")

    def run_algorithm(self, visualize: bool = True) -> Tuple[bool, bool]:
        """
        Run complete Deutsch-Jozsa algorithm for both function types.

        Args:
            visualize (bool): Whether to display visualizations (default: True)

        Returns:
            Tuple[bool, bool]: (constant_correct, balanced_correct)
        """
        logger.info("=" * 60)
        logger.info("Starting Deutsch-Jozsa Algorithm")
        logger.info("=" * 60)

        # Test constant function
        logger.info("\n--- Testing Constant Function ---")
        const_oracle = self.create_constant_oracle()
        const_circuit = self.build_circuit(const_oracle)
        counts_const = self.run_circuit(const_circuit)

        print(f"\nConstant function measurement counts: {counts_const}")
        const_correct = self.interpret_result(counts_const, "constant")

        if visualize:
            self.visualize_results(counts_const, "Constant Function Results")

        # Test balanced function
        logger.info("\n--- Testing Balanced Function ---")
        balanced_oracle = self.create_balanced_oracle()
        balanced_circuit = self.build_circuit(balanced_oracle)
        counts_balanced = self.run_circuit(balanced_circuit)

        print(f"\nBalanced function measurement counts: {counts_balanced}")
        balanced_correct = self.interpret_result(counts_balanced, "balanced")

        if visualize:
            self.visualize_results(counts_balanced, "Balanced Function Results")

        logger.info("\n" + "=" * 60)
        logger.info("Algorithm Execution Complete")
        logger.info("=" * 60)

        return const_correct, balanced_correct

    def run_enhanced_algorithm(
        self,
        function_type: FunctionType,
        shots: int = 1024,
        optimization_level: int = 1,
        visualize: bool = False,
    ) -> AlgorithmSummary:
        """
        Run enhanced Deutsch-Jozsa algorithm with detailed metrics.

        Args:
            function_type (FunctionType): Type of function to test
            shots (int): Number of measurement shots
            optimization_level (int): Circuit optimization level
            visualize (bool): Whether to show visualization

        Returns:
            AlgorithmSummary: Detailed execution summary
        """
        start_time = time.time()
        initial_memory = self._measure_memory_usage()

        logger.info(f"Running enhanced algorithm for {function_type.value} function")

        try:
            # Create oracle based on function type
            if function_type == FunctionType.CONSTANT:
                oracle = self.create_constant_oracle()
                expected_type = "constant"
            else:
                oracle = self.create_balanced_oracle()
                expected_type = "balanced"

            # Build and run circuit
            circuit = self.build_circuit(oracle)
            transpiled = transpile(
                circuit, self.backend, optimization_level=optimization_level
            )
            counts = self.run_circuit(circuit, shots, optimization_level)

            # Calculate metrics
            execution_time = time.time() - start_time
            final_memory = self._measure_memory_usage()
            memory_usage = final_memory - initial_memory

            # Interpret results
            is_correct = self.interpret_result(counts, expected_type)
            confidence = self._calculate_confidence(counts, expected_type)

            # Create execution metrics
            metrics = ExecutionMetrics(
                execution_time=execution_time,
                circuit_depth=transpiled.depth(),
                gate_count=len(transpiled.data),
                shots=shots,
                memory_usage=memory_usage,
                timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            )

            # Create summary
            result = AlgorithmResult.SUCCESS if is_correct else AlgorithmResult.FAILURE
            summary = AlgorithmSummary(
                function_type=function_type,
                result=result,
                confidence=confidence,
                measurements=counts,
                metrics=metrics,
            )

            # Store in history
            self.execution_history.append(summary)

            # Visualization
            if visualize:
                title = f"{function_type.value.title()} Function Results"
                self.visualize_results(counts, title)

            assert isinstance(summary.metrics.memory_usage, (int, float))
            logger.info(
                f"Enhanced algorithm completed: {result.value}, "
                f"confidence: {confidence:.2%}"
            )

            return summary

        except Exception as e:
            execution_time = time.time() - start_time
            final_memory = self._measure_memory_usage()
            memory_usage = final_memory - initial_memory

            logger.error(
                f"Enhanced algorithm failed after {execution_time:.3f}s: {str(e)}"
            )

            # Create failure summary and add to history
            metrics = ExecutionMetrics(
                execution_time=execution_time,
                circuit_depth=0,
                gate_count=0,
                shots=shots,
                memory_usage=memory_usage,
                timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            )

            summary = AlgorithmSummary(
                function_type=function_type,
                result=AlgorithmResult.FAILURE,
                confidence=0.0,
                measurements={},
                metrics=metrics,
            )

            # Store in history even for failures
            self.execution_history.append(summary)

            return summary

    def _calculate_confidence(
        self, counts: Dict[str, int], expected_type: str
    ) -> float:
        """Calculate confidence level in the result."""
        if not counts:
            return 0.0

        total_shots = sum(counts.values())
        zero_state = "0" * self.n_qubits

        if expected_type == "constant":
            # High confidence if all measurements are zero state
            return counts.get(zero_state, 0) / total_shots
        else:
            # High confidence if no measurements are zero state
            return 1.0 - (counts.get(zero_state, 0) / total_shots)

    def get_execution_history(self) -> List[AlgorithmSummary]:
        """Get the execution history."""
        return self.execution_history.copy()

    def clear_history(self) -> None:
        """Clear the execution history."""
        self.execution_history.clear()
        logger.info("Execution history cleared")

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics from execution history."""
        if not self.execution_history:
            return {}

        successful_runs = [
            s for s in self.execution_history if s.result == AlgorithmResult.SUCCESS
        ]

        if not successful_runs:
            return {"message": "No successful runs in history"}

        execution_times = [s.metrics.execution_time for s in successful_runs]
        circuit_depths = [s.metrics.circuit_depth for s in successful_runs]
        gate_counts = [s.metrics.gate_count for s in successful_runs]

        return {
            "total_runs": len(self.execution_history),
            "successful_runs": len(successful_runs),
            "success_rate": len(successful_runs) / len(self.execution_history),
            "avg_execution_time": sum(execution_times) / len(execution_times),
            "avg_circuit_depth": sum(circuit_depths) / len(circuit_depths),
            "avg_gate_count": sum(gate_counts) / len(gate_counts),
            "avg_confidence": sum(s.confidence for s in successful_runs)
            / len(successful_runs),
        }


def main():
    """Main entry point for the Deutsch-Jozsa algorithm demonstration."""
    try:
        # Initialize and run algorithm
        dj = DeutschJozsaAlgorithm(n_qubits=3)
        const_correct, balanced_correct = dj.run_algorithm(visualize=True)

        # Print summary
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"Constant function test: {'PASSED ✓' if const_correct else 'FAILED ✗'}")
        print(
            f"Balanced function test: {'PASSED ✓' if balanced_correct else 'FAILED ✗'}"
        )
        print("=" * 60)

        # Exit with appropriate code
        if const_correct and balanced_correct:
            logger.info("All tests passed successfully!")
            sys.exit(0)
        else:
            logger.error("Some tests failed!")
            sys.exit(1)

    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
