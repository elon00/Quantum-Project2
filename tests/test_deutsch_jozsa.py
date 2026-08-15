"""
Unit tests for Deutsch-Jozsa Algorithm implementation.

This module contains comprehensive unit tests for all components
of the Deutsch-Jozsa quantum algorithm including enhanced features.
"""

from unittest.mock import patch

import pytest
from qiskit import QuantumCircuit

from deutsch_jozsa import (
    AlgorithmResult,
    AlgorithmSummary,
    DeutschJozsaAlgorithm,
    ExecutionMetrics,
    FunctionType,
)


class TestDeutschJozsaAlgorithmInit:
    """Test suite for DeutschJozsaAlgorithm initialization."""

    def test_init_default_qubits(self):
        """Test initialization with default number of qubits."""
        dj = DeutschJozsaAlgorithm()
        assert dj.n_qubits == 3
        assert dj.backend is not None

    def test_init_custom_qubits(self):
        """Test initialization with custom number of qubits."""
        dj = DeutschJozsaAlgorithm(n_qubits=5)
        assert dj.n_qubits == 5

    def test_init_single_qubit(self):
        """Test initialization with single qubit."""
        dj = DeutschJozsaAlgorithm(n_qubits=1)
        assert dj.n_qubits == 1

    def test_init_invalid_qubits_zero(self):
        """Test that initialization fails with zero qubits."""
        with pytest.raises(ValueError, match="Number of qubits must be at least 1"):
            DeutschJozsaAlgorithm(n_qubits=0)

    def test_init_invalid_qubits_negative(self):
        """Test that initialization fails with negative qubits."""
        with pytest.raises(ValueError, match="Number of qubits must be at least 1"):
            DeutschJozsaAlgorithm(n_qubits=-1)


class TestCircuitCreation:
    """Test suite for quantum circuit creation methods."""

    def test_create_base_circuit_structure(self):
        """Test that base circuit has correct structure."""
        dj = DeutschJozsaAlgorithm(n_qubits=3)
        circuit = dj.create_base_circuit()

        assert isinstance(circuit, QuantumCircuit)
        assert circuit.num_qubits == 4  # 3 input + 1 output
        assert circuit.num_clbits == 3  # 3 classical bits for measurement

    def test_create_base_circuit_gates(self):
        """Test that base circuit contains expected gates."""
        dj = DeutschJozsaAlgorithm(n_qubits=2)
        circuit = dj.create_base_circuit()

        # Check that circuit has gates (X and H gates)
        assert len(circuit.data) > 0

    def test_create_constant_oracle(self):
        """Test constant oracle creation."""
        dj = DeutschJozsaAlgorithm(n_qubits=3)
        oracle = dj.create_constant_oracle()

        assert isinstance(oracle, QuantumCircuit)
        assert oracle.num_qubits == 4
        # Constant oracle should have no gates
        assert len(oracle.data) == 0

    def test_create_balanced_oracle(self):
        """Test balanced oracle creation."""
        dj = DeutschJozsaAlgorithm(n_qubits=3)
        oracle = dj.create_balanced_oracle()

        assert isinstance(oracle, QuantumCircuit)
        assert oracle.num_qubits == 4
        # Balanced oracle should have CNOT gates
        assert len(oracle.data) == 3  # One CNOT per input qubit

    def test_build_circuit_with_constant_oracle(self):
        """Test building complete circuit with constant oracle."""
        dj = DeutschJozsaAlgorithm(n_qubits=3)
        oracle = dj.create_constant_oracle()
        circuit = dj.build_circuit(oracle)

        assert isinstance(circuit, QuantumCircuit)
        assert circuit.num_qubits == 4
        assert circuit.num_clbits == 3

    def test_build_circuit_with_balanced_oracle(self):
        """Test building complete circuit with balanced oracle."""
        dj = DeutschJozsaAlgorithm(n_qubits=3)
        oracle = dj.create_balanced_oracle()
        circuit = dj.build_circuit(oracle)

        assert isinstance(circuit, QuantumCircuit)
        assert circuit.num_qubits == 4
        assert circuit.num_clbits == 3


class TestCircuitExecution:
    """Test suite for circuit execution methods."""

    def test_run_circuit_returns_counts(self):
        """Test that run_circuit returns measurement counts."""
        dj = DeutschJozsaAlgorithm(n_qubits=3)
        oracle = dj.create_constant_oracle()
        circuit = dj.build_circuit(oracle)

        counts = dj.run_circuit(circuit, shots=100)

        assert isinstance(counts, dict)
        assert len(counts) > 0
        assert all(isinstance(k, str) for k in counts.keys())
        assert all(isinstance(v, int) for v in counts.values())

    def test_run_circuit_custom_shots(self):
        """Test circuit execution with custom number of shots."""
        dj = DeutschJozsaAlgorithm(n_qubits=2)
        oracle = dj.create_constant_oracle()
        circuit = dj.build_circuit(oracle)

        shots = 500
        counts = dj.run_circuit(circuit, shots=shots)

        total_counts = sum(counts.values())
        assert total_counts == shots

    def test_run_circuit_constant_oracle_result(self):
        """Test that constant oracle produces all-zero measurements."""
        dj = DeutschJozsaAlgorithm(n_qubits=3)
        oracle = dj.create_constant_oracle()
        circuit = dj.build_circuit(oracle)

        counts = dj.run_circuit(circuit, shots=1024)

        # Constant function should measure all zeros
        assert "000" in counts
        assert len(counts) == 1

    def test_run_circuit_balanced_oracle_result(self):
        """Test that balanced oracle produces non-zero measurements."""
        dj = DeutschJozsaAlgorithm(n_qubits=3)
        oracle = dj.create_balanced_oracle()
        circuit = dj.build_circuit(oracle)

        counts = dj.run_circuit(circuit, shots=1024)

        # Balanced function should not measure all zeros
        assert "000" not in counts or len(counts) > 1


class TestResultInterpretation:
    """Test suite for result interpretation methods."""

    def test_interpret_constant_correct(self):
        """Test correct interpretation of constant function."""
        dj = DeutschJozsaAlgorithm(n_qubits=3)
        counts = {"000": 1024}

        result = dj.interpret_result(counts, "constant")
        assert result is True

    def test_interpret_constant_incorrect(self):
        """Test incorrect interpretation of constant function."""
        dj = DeutschJozsaAlgorithm(n_qubits=3)
        counts = {"111": 1024}

        result = dj.interpret_result(counts, "constant")
        assert result is False

    def test_interpret_balanced_correct(self):
        """Test correct interpretation of balanced function."""
        dj = DeutschJozsaAlgorithm(n_qubits=3)
        counts = {"111": 1024}

        result = dj.interpret_result(counts, "balanced")
        assert result is True

    def test_interpret_balanced_incorrect(self):
        """Test incorrect interpretation of balanced function."""
        dj = DeutschJozsaAlgorithm(n_qubits=3)
        counts = {"000": 1024}

        result = dj.interpret_result(counts, "balanced")
        assert result is False

    def test_interpret_invalid_function_type(self):
        """Test that invalid function type raises error."""
        dj = DeutschJozsaAlgorithm(n_qubits=3)
        counts = {"000": 1024}

        with pytest.raises(ValueError, match="Unknown function type"):
            dj.interpret_result(counts, "invalid")


class TestVisualization:
    """Test suite for visualization methods."""

    @patch("deutsch_jozsa.plt.show")
    @patch("deutsch_jozsa.plot_histogram")
    def test_visualize_results_no_save(self, mock_plot, mock_show):
        """Test visualization without saving."""
        dj = DeutschJozsaAlgorithm(n_qubits=3)
        counts = {"000": 1024}

        dj.visualize_results(counts, "Test Title")

        mock_plot.assert_called_once_with(counts)
        mock_show.assert_called_once()

    @patch("deutsch_jozsa.plt.savefig")
    @patch("deutsch_jozsa.plt.show")
    @patch("deutsch_jozsa.plot_histogram")
    def test_visualize_results_with_save(self, mock_plot, mock_show, mock_savefig):
        """Test visualization with saving to file."""
        dj = DeutschJozsaAlgorithm(n_qubits=3)
        counts = {"000": 1024}

        dj.visualize_results(counts, "Test Title", save_path="test.png")

        mock_plot.assert_called_once_with(counts)
        mock_savefig.assert_called_once()
        mock_show.assert_called_once()


class TestFullAlgorithm:
    """Test suite for complete algorithm execution."""

    def test_run_algorithm_returns_tuple(self):
        """Test that run_algorithm returns tuple of results."""
        dj = DeutschJozsaAlgorithm(n_qubits=2)

        with patch.object(dj, "visualize_results"):
            result = dj.run_algorithm(visualize=False)

        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], bool)
        assert isinstance(result[1], bool)

    def test_run_algorithm_constant_passes(self):
        """Test that constant function test passes."""
        dj = DeutschJozsaAlgorithm(n_qubits=3)

        with patch.object(dj, "visualize_results"):
            const_correct, _ = dj.run_algorithm(visualize=False)

        assert const_correct is True

    def test_run_algorithm_balanced_passes(self):
        """Test that balanced function test passes."""
        dj = DeutschJozsaAlgorithm(n_qubits=3)

        with patch.object(dj, "visualize_results"):
            _, balanced_correct = dj.run_algorithm(visualize=False)

        assert balanced_correct is True

    def test_run_algorithm_with_visualization(self):
        """Test algorithm execution with visualization enabled."""
        dj = DeutschJozsaAlgorithm(n_qubits=2)

        with patch.object(dj, "visualize_results") as mock_viz:
            dj.run_algorithm(visualize=True)

            # Should be called twice (constant and balanced)
            assert mock_viz.call_count == 2

    def test_run_algorithm_without_visualization(self):
        """Test algorithm execution with visualization disabled."""
        dj = DeutschJozsaAlgorithm(n_qubits=2)

        with patch.object(dj, "visualize_results") as mock_viz:
            dj.run_algorithm(visualize=False)

            # Should not be called
            mock_viz.assert_not_called()


class TestEdgeCases:
    """Test suite for edge cases and error handling."""

    def test_single_qubit_algorithm(self):
        """Test algorithm with single qubit."""
        dj = DeutschJozsaAlgorithm(n_qubits=1)

        with patch.object(dj, "visualize_results"):
            const_correct, balanced_correct = dj.run_algorithm(visualize=False)

        assert isinstance(const_correct, bool)
        assert isinstance(balanced_correct, bool)

    def test_large_number_of_qubits(self):
        """Test algorithm with larger number of qubits."""
        dj = DeutschJozsaAlgorithm(n_qubits=5)

        oracle = dj.create_constant_oracle()
        circuit = dj.build_circuit(oracle)

        assert circuit.num_qubits == 6
        assert circuit.num_clbits == 5

    def test_minimal_shots(self):
        """Test circuit execution with minimal shots."""
        dj = DeutschJozsaAlgorithm(n_qubits=2)
        oracle = dj.create_constant_oracle()
        circuit = dj.build_circuit(oracle)

        counts = dj.run_circuit(circuit, shots=1)

        assert sum(counts.values()) == 1


class TestIntegration:
    """Integration tests for complete workflows."""

    def test_complete_workflow_constant(self):
        """Test complete workflow for constant function."""
        dj = DeutschJozsaAlgorithm(n_qubits=3)

        # Create oracle
        oracle = dj.create_constant_oracle()

        # Build circuit
        circuit = dj.build_circuit(oracle)

        # Run circuit
        counts = dj.run_circuit(circuit)

        # Interpret results
        is_correct = dj.interpret_result(counts, "constant")

        assert is_correct is True

    def test_complete_workflow_balanced(self):
        """Test complete workflow for balanced function."""
        dj = DeutschJozsaAlgorithm(n_qubits=3)

        # Create oracle
        oracle = dj.create_balanced_oracle()

        # Build circuit
        circuit = dj.build_circuit(oracle)

        # Run circuit
        counts = dj.run_circuit(circuit)

        # Interpret results
        is_correct = dj.interpret_result(counts, "balanced")

        assert is_correct is True

    def test_multiple_runs_consistency(self):
        """Test that multiple runs produce consistent results."""
        dj = DeutschJozsaAlgorithm(n_qubits=3)
        oracle = dj.create_constant_oracle()
        circuit = dj.build_circuit(oracle)

        results = []
        for _ in range(5):
            counts = dj.run_circuit(circuit, shots=100)
            is_correct = dj.interpret_result(counts, "constant")
            results.append(is_correct)

        # All runs should produce consistent results
        assert all(results)


class TestEnhancedFeatures:
    """Test suite for enhanced algorithm features."""

    def test_enhanced_algorithm_constant_function(self):
        """Test enhanced algorithm with constant function."""
        dj = DeutschJozsaAlgorithm(n_qubits=2)

        summary = dj.run_enhanced_algorithm(FunctionType.CONSTANT, shots=100)

        assert isinstance(summary, AlgorithmSummary)
        assert summary.function_type == FunctionType.CONSTANT
        assert summary.result == AlgorithmResult.SUCCESS
        assert summary.confidence == 1.0
        assert "00" in summary.measurements
        assert summary.metrics.execution_time > 0
        assert summary.metrics.circuit_depth > 0
        assert summary.metrics.gate_count > 0

    def test_enhanced_algorithm_balanced_function(self):
        """Test enhanced algorithm with balanced function."""
        dj = DeutschJozsaAlgorithm(n_qubits=2)

        summary = dj.run_enhanced_algorithm(FunctionType.BALANCED, shots=100)

        assert isinstance(summary, AlgorithmSummary)
        assert summary.function_type == FunctionType.BALANCED
        assert summary.result == AlgorithmResult.SUCCESS
        assert summary.confidence == 1.0
        assert "00" not in summary.measurements or len(summary.measurements) > 1
        assert summary.metrics.execution_time > 0

    def test_enhanced_algorithm_with_optimization(self):
        """Test enhanced algorithm with different optimization levels."""
        dj = DeutschJozsaAlgorithm(n_qubits=2)

        # Test different optimization levels
        for opt_level in [0, 1, 2, 3]:
            summary = dj.run_enhanced_algorithm(
                FunctionType.CONSTANT, shots=50, optimization_level=opt_level
            )

            assert isinstance(summary, AlgorithmSummary)
            assert summary.metrics.circuit_depth > 0

    def test_execution_history_tracking(self):
        """Test that execution history is properly tracked."""
        dj = DeutschJozsaAlgorithm(n_qubits=2)

        # Initially empty
        assert len(dj.get_execution_history()) == 0

        # Run algorithm
        summary1 = dj.run_enhanced_algorithm(FunctionType.CONSTANT, shots=50)
        summary2 = dj.run_enhanced_algorithm(FunctionType.BALANCED, shots=50)

        # Check history
        history = dj.get_execution_history()
        assert len(history) == 2
        assert history[0] == summary1
        assert history[1] == summary2

    def test_clear_history(self):
        """Test clearing execution history."""
        dj = DeutschJozsaAlgorithm(n_qubits=2)

        # Add some history
        dj.run_enhanced_algorithm(FunctionType.CONSTANT, shots=50)
        assert len(dj.get_execution_history()) == 1

        # Clear history
        dj.clear_history()
        assert len(dj.get_execution_history()) == 0

    def test_performance_stats_calculation(self):
        """Test performance statistics calculation."""
        dj = DeutschJozsaAlgorithm(n_qubits=2)

        # Run multiple algorithms
        for _ in range(3):
            dj.run_enhanced_algorithm(FunctionType.CONSTANT, shots=50)

        stats = dj.get_performance_stats()

        assert "total_runs" in stats
        assert "successful_runs" in stats
        assert "success_rate" in stats
        assert "avg_execution_time" in stats
        assert stats["total_runs"] == 3
        assert stats["successful_runs"] == 3
        assert stats["success_rate"] == 1.0

    def test_custom_backend_support(self):
        """Test algorithm with custom backend."""
        from qiskit_aer import AerSimulator

        custom_backend = AerSimulator()
        dj = DeutschJozsaAlgorithm(n_qubits=2, backend=custom_backend)

        summary = dj.run_enhanced_algorithm(FunctionType.CONSTANT, shots=50)

        assert isinstance(summary, AlgorithmSummary)
        assert summary.result == AlgorithmResult.SUCCESS

    def test_memory_usage_tracking(self):
        """Test memory usage tracking."""
        dj = DeutschJozsaAlgorithm(n_qubits=2)

        summary = dj.run_enhanced_algorithm(FunctionType.CONSTANT, shots=50)

        # Memory usage should be tracked (might be 0 if psutil not available)
        assert isinstance(summary.metrics.memory_usage, (int, float))
        assert (
            summary.metrics.memory_usage >= 0.0
        ), f"Expected non-negative memory usage, got {summary.metrics.memory_usage}"

    def test_confidence_calculation(self):
        """Test confidence calculation for different scenarios."""
        dj = DeutschJozsaAlgorithm(n_qubits=2)

        # Test constant function with perfect results
        counts_perfect = {"00": 100}
        confidence = dj._calculate_confidence(counts_perfect, "constant")
        assert confidence == 1.0

        # Test constant function with imperfect results
        counts_imperfect = {"00": 80, "01": 20}
        confidence = dj._calculate_confidence(counts_imperfect, "constant")
        assert confidence == 0.8

        # Test balanced function with perfect results
        counts_balanced = {"01": 50, "10": 50}
        confidence = dj._calculate_confidence(counts_balanced, "balanced")
        assert confidence == 1.0

    def test_enhanced_algorithm_failure_handling(self):
        """Test enhanced algorithm failure handling."""
        dj = DeutschJozsaAlgorithm(n_qubits=2)

        # Mock a backend failure
        with patch.object(dj.backend, "run", side_effect=Exception("Backend error")):
            summary = dj.run_enhanced_algorithm(FunctionType.CONSTANT, shots=50)

            assert summary.result == AlgorithmResult.FAILURE
            assert summary.confidence == 0.0
            assert summary.measurements == {}

    def test_algorithm_summary_data_integrity(self):
        """Test that algorithm summary maintains data integrity."""
        dj = DeutschJozsaAlgorithm(n_qubits=2)

        summary = dj.run_enhanced_algorithm(FunctionType.CONSTANT, shots=100)

        # Check that all fields are properly populated
        assert summary.function_type in [FunctionType.CONSTANT, FunctionType.BALANCED]
        assert summary.result in [
            AlgorithmResult.SUCCESS,
            AlgorithmResult.FAILURE,
            AlgorithmResult.INCONCLUSIVE,
        ]
        assert 0.0 <= summary.confidence <= 1.0
        assert isinstance(summary.measurements, dict)
        assert isinstance(summary.metrics, ExecutionMetrics)
        assert summary.metrics.execution_time > 0
        assert summary.metrics.shots == 100
        assert isinstance(summary.metrics.timestamp, str)


class TestEdgeCasesEnhanced:
    """Test suite for enhanced edge cases."""

    def test_single_qubit_enhanced_algorithm(self):
        """Test enhanced algorithm with single qubit."""
        dj = DeutschJozsaAlgorithm(n_qubits=1)

        summary = dj.run_enhanced_algorithm(FunctionType.CONSTANT, shots=50)

        assert isinstance(summary, AlgorithmSummary)
        assert summary.function_type == FunctionType.CONSTANT

    def test_large_qubit_enhanced_algorithm(self):
        """Test enhanced algorithm with larger number of qubits."""
        dj = DeutschJozsaAlgorithm(n_qubits=4)

        summary = dj.run_enhanced_algorithm(FunctionType.BALANCED, shots=100)

        assert isinstance(summary, AlgorithmSummary)
        assert summary.function_type == FunctionType.BALANCED
        assert summary.metrics.circuit_depth > 0

    def test_very_small_shots(self):
        """Test enhanced algorithm with very small number of shots."""
        dj = DeutschJozsaAlgorithm(n_qubits=2)

        summary = dj.run_enhanced_algorithm(FunctionType.CONSTANT, shots=1)

        assert isinstance(summary, AlgorithmSummary)
        assert summary.metrics.shots == 1

    def test_performance_stats_with_failures(self):
        """Test performance stats calculation with some failures."""
        dj = DeutschJozsaAlgorithm(n_qubits=2)

        # Add successful run
        dj.run_enhanced_algorithm(FunctionType.CONSTANT, shots=50)

        # Add failed run
        with patch.object(dj.backend, "run", side_effect=Exception("Backend error")):
            dj.run_enhanced_algorithm(FunctionType.BALANCED, shots=50)

        stats = dj.get_performance_stats()

        assert stats["total_runs"] == 2
        assert stats["successful_runs"] == 1
        assert stats["success_rate"] == 0.5


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=deutsch_jozsa", "--cov-report=term-missing"])
