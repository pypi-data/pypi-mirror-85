import numpy as np
from qiskit.circuit import ParameterVector
from qiskit.aqua.algorithms.classifiers import QSVM 

def get_qiskit_state_vectors(quantum_instance, feature_map, x):
    is_statevector_sim = quantum_instance.is_statevector

    measurement = not is_statevector_sim
    measurement_basis = '0' * feature_map.num_qubits

        
    # build parameterized circuits, it could be slower for building circuit
    # but overall it should be faster since it only transpile one circuit
    feature_map_params = ParameterVector('x', feature_map.feature_dimension)
    parameterized_circuit = QSVM._construct_circuit(
        (feature_map_params, feature_map_params), feature_map, measurement,
        is_statevector_sim=is_statevector_sim)
    parameterized_circuit = quantum_instance.transpile(parameterized_circuit)[0]
    circuits = [parameterized_circuit.assign_parameters({feature_map_params: params})
                for params in x]        
    results = quantum_instance.execute(circuits, had_transpiled=True) 
    statevectors = np.array([results.get_statevector(i) for i in range(len(results.results))])
    return statevectors
