from qiskit.circuit.library import PauliFeatureMap 
from qiskit import QuantumCircuit
from quple.components.interaction_graphs import interaction_graph

class FeatureMapDev(PauliFeatureMap):
    def pauli_evolution(self, pauli_string, time):
        """Get the evolution block for the given pauli string."""
        # for some reason this is in reversed order
        pauli_string = pauli_string[::-1]

        # trim the pauli string if identities are included
        trimmed = []
        indices = []
        for i, pauli in enumerate(pauli_string):
            if pauli != 'I':
                trimmed += [pauli]
                indices += [i]

        evo = QuantumCircuit(len(pauli_string))

        if len(trimmed) == 0:
            return evo

        def basis_change(circuit, inverse=False):
            # do not change basis if only first order pauli operator
            if len(pauli_string) == 1:
                return
            for i, pauli in enumerate(pauli_string):
                if pauli == 'X':
                    circuit.h(i)
                elif pauli == 'Y':
                    circuit.rx(-np.pi / 2 if inverse else np.pi / 2, i)

        def cx_chain(circuit, inverse=False):
            num_cx = len(indices) - 1
            for i in reversed(range(num_cx)) if inverse else range(num_cx):
                circuit.cx(indices[i], indices[i + 1])

        basis_change(evo)
        cx_chain(evo)
        if len(pauli_string) == 1:
            if pauli_string[0] == 'Z':
                evo.rz(time, indices[-1])
            elif pauli_string[0] == 'X':
                evo.rx(time, indices[-1])
            elif pauli_string[0] == 'Y':
                evo.ry(time, indices[-1])
        else:
            evo.rz(time, indices[-1])
        cx_chain(evo, inverse=True)
        basis_change(evo, inverse=True)
        return evo
    
    def get_entangler_map(self, rep_num: int, 
                          block_num: int, num_block_qubits: int) :
        strategy = self.entanglement
        if isinstance(strategy, str):
            return interaction_graph[strategy](self.num_qubits, num_block_qubits)
        elif callable(strategy):
            return strategy(self.num_qubits, num_block_qubits)
        elif isinstance(strategy, list):
            if all(isinstance(strat, str) for strat in strategy):
                return interaction_graph[strategy[block_num]](self.num_qubits, num_block_qubits)
            elif all(callable(strat) for strat in strategy):
                return strategy[block_num](self.num_qubits, num_block_qubits)
        else:
            raise ValueError('invalid entangle strategy: {}'.format(strategy))