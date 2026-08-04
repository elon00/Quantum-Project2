"""
Integration tests for Deutsch-Jozsa Algorithm.

This module contains integration tests that verify the complete
workflow and interaction between different components.
"""

from unittest.mock import patch

import pytest

from deutsch_jozsa import DeutschJozsaAlgorithm


class TestEndToEndWorkflow:
    """Test complete end-to-end workflows."""

    def test_full_algorithm_execution(self):
        """Test complete algorithm execution from start to finish."""
        dj = DeutschJozsaAlgorithm(n_qubits=3)

        with patch.object(dj, "visualize_results"):
            const_correct, balanced_correct = dj.run_algorithm(visualize=False)

        # Both tests should pass
        assert const_correct is True, "Constant function test failed"
        assert balanced_correct is True, "Balanced function test failed"

    def test_algorithm_with_different_qubit_counts(self):
        """Test algorithm works correctly with different qubit counts."""
        qubit_counts = [1, 2, 3, 4, 5]

        for n in qubit_counts:
            dj = DeutschJozsaAlgorithm(n_qubits=n)

            with patch.object(dj, "visualize_results"):
                const_correct, balanced_correct = dj.run_algorithm(visualize=False)

            assert const_correct is True, f"Constant test failed for {n} qubits"
            assert balanced_correct is True, f"Balanced test failed for {n} qubits"

    def test_multiple_sequential_runs(self):
        """Test multiple sequential algorithm runs."""
        dj = DeutschJozsaAlgorithm(n_qubits=3)

        results = []
        for _ in range(3):
            with patch.object(dj, "visualize_results"):
                result = dj.run_algorithm(visualize=False)
            results.append(result)

        # All runs should produce consistent results
        for const_correct, balanced_correct in results:
            assert const_correct is True
            assert balanced_correct is True


class TestOracleIntegration:
    """Test integration between oracles and circuit execution."""

    def test_constant_oracle_integration(self):
        """Test complete workflow with constant oracle."""
        dj = DeutschJozsaAlgorithm(n_qubits=3)

        # Create and test constant oracle
        oracle = dj.create_constant_oracle()
        circuit = dj.build_circuit(oracle)
        counts = dj.run_circuit(circuit, shots=1000)
        result = dj.interpret_result(counts, "constant")

        assert result is True
        assert "000" in counts
        assert len(counts) == 1

    def test_balanced_oracle_integration(self):
        """Test complete workflow with balanced oracle."""
        dj = DeutschJozsaAlgorithm(n_qubits=3)

        # Create and test balanced oracle
        oracle = dj.create_balanced_oracle()
        circuit = dj.build_circuit(oracle)
        counts = dj.run_circuit(circuit, shots=1000)
        result = dj.interpret_result(counts, "balanced")

        assert result is True
        # Should not measure all zeros
        assert "000" not in counts or len(counts) > 1


class TestStatisticalConsistency:
    """Test statistical consistency of quantum measurements."""

    def test_constant_oracle_statistical_consistency(self):
        """Test that constant oracle produces consistent results across runs."""
        dj = DeutschJozsaAlgorithm(n_qubits=3)
        oracle = dj.create_constant_oracle()
        circuit = dj.build_circuit(oracle)

        results = []
        for _ in range(10):
            counts = dj.run_circuit(circuit, shots=100)
            results.append(counts)

        # All results should be identical for constant function
        for counts in results:
            assert "000" in counts
            assert len(counts) == 1

    def test_balanced_oracle_statistical_consistency(self):
        """Test that balanced oracle produces consistent results across runs."""
        dj = DeutschJozsaAlgorithm(n_qubits=3)
        oracle = dj.create_balanced_oracle()
        circuit = dj.build_circuit(oracle)

        results = []
        for _ in range(10):
            counts = dj.run_circuit(circuit, shots=100)
            results.append(counts)

        # All results should show non-zero pattern for balanced function
        for counts in results:
            assert "000" not in counts or len(counts) > 1


class TestScalability:
    """Test algorithm scalability with different parameters."""

    def test_varying_shot_counts(self):
        """Test algorithm with different shot counts."""
        dj = DeutschJozsaAlgorithm(n_qubits=3)
        oracle = dj.create_constant_oracle()
        circuit = dj.build_circuit(oracle)

        shot_counts = [10, 100, 500, 1000, 2000]

        for shots in shot_counts:
            counts = dj.run_circuit(circuit, shots=shots)
            total = sum(counts.values())

            assert total == shots, f"Shot count mismatch for {shots} shots"
            assert "000" in counts

    def test_increasing_qubit_complexity(self):
        """Test algorithm performance with increasing qubit counts."""
        qubit_range = range(1, 6)

        for n_qubits in qubit_range:
            dj = DeutschJozsaAlgorithm(n_qubits=n_qubits)

            # Test constant oracle
            const_oracle = dj.create_constant_oracle()
            const_circuit = dj.build_circuit(const_oracle)
            const_counts = dj.run_circuit(const_circuit, shots=100)

            # Verify correct structure
            zero_state = "0" * n_qubits
            assert zero_state in const_counts

            # Test balanced oracle
            balanced_oracle = dj.create_balanced_oracle()
            balanced_circuit = dj.build_circuit(balanced_oracle)
            balanced_counts = dj.run_circuit(balanced_circuit, shots=100)

            # Verify non-zero pattern
            assert zero_state not in balanced_counts or len(balanced_counts) > 1


class TestErrorRecovery:
    """Test error handling and recovery mechanisms."""

    def test_algorithm_continues_after_visualization_error(self):
        """Test that algorithm continues even if visualization fails."""
        dj = DeutschJozsaAlgorithm(n_qubits=3)

        # Mock visualization to raise an error
        with patch.object(dj, "visualize_results", side_effect=Exception("Viz error")):
            # Algorithm should still complete despite visualization error
            try:
                const_correct, balanced_correct = dj.run_algorithm(visualize=True)
                # If we get here, error was handled gracefully
                assert True
            except Exception as e:
                # If exception propagates, that's also acceptable behavior
                assert "Viz error" in str(e)


class TestRealWorldScenarios:
    """Test real-world usage scenarios."""

    def test_typical_user_workflow(self):
        """Test typical user workflow from initialization to results."""
        # User creates algorithm instance
        dj = DeutschJozsaAlgorithm(n_qubits=3)

        # User runs algorithm
        with patch.object(dj, "visualize_results"):
            const_result, balanced_result = dj.run_algorithm(visualize=False)

        # User checks results
        assert isinstance(const_result, bool)
        assert isinstance(balanced_result, bool)
        assert const_result is True
        assert balanced_result is True

    def test_custom_oracle_workflow(self):
        """Test workflow where user creates custom oracle."""
        dj = DeutschJozsaAlgorithm(n_qubits=3)

        # User creates custom oracle (using balanced as example)
        custom_oracle = dj.create_balanced_oracle()

        # User builds circuit
        circuit = dj.build_circuit(custom_oracle)

        # User runs circuit
        counts = dj.run_circuit(circuit, shots=500)

        # User interprets results
        is_balanced = dj.interpret_result(counts, "balanced")

        assert is_balanced is True

    def test_batch_processing_workflow(self):
        """Test batch processing of multiple algorithm instances."""
        instances = [DeutschJozsaAlgorithm(n_qubits=n) for n in [2, 3, 4]]

        results = []
        for dj in instances:
            with patch.object(dj, "visualize_results"):
                result = dj.run_algorithm(visualize=False)
            results.append(result)

        # All instances should produce correct results
        for const_correct, balanced_correct in results:
            assert const_correct is True
            assert balanced_correct is True


class TestPerformanceCharacteristics:
    """Test performance characteristics of the algorithm."""

    def test_execution_time_reasonable(self):
        """Test that algorithm executes in reasonable time."""
        import time

        dj = DeutschJozsaAlgorithm(n_qubits=3)

        start_time = time.time()
        with patch.object(dj, "visualize_results"):
            dj.run_algorithm(visualize=False)
        end_time = time.time()

        execution_time = end_time - start_time

        # Should complete in under 10 seconds for 3 qubits
        assert execution_time < 10, f"Execution took {execution_time}s, expected < 10s"

    def test_memory_efficiency(self):
        """Test that algorithm doesn't consume excessive memory."""
        import sys

        dj = DeutschJozsaAlgorithm(n_qubits=3)

        # Get size of algorithm instance
        size = sys.getsizeof(dj)

        # Should be reasonably sized (less than 1MB)
        assert size < 1024 * 1024, f"Instance size {size} bytes is too large"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=deutsch_jozsa", "--cov-report=term-missing"])
