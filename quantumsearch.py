from qiskit import * 
from qiskit.tools.visualization import plot_histogram
# %matplotlib inline
from qiskit.circuit.library import QFT
import math

def initialization(target_states):
    # Number of quibits
    n = len(target_states[0])
    init_circuit = QuantumCircuit(n, name="INIT")
    init_circuit.h(list(range(n)))
    init_circuit.to_gate()
     
    return init_circuit

def grover_oracle(target_states):
    # Number of qubits
    n = len(target_states[0]) 
    
    # Create a quantum circuit, number of qubits and number of classical bits
    oracle = QuantumCircuit(n,name="Oracle")
    
    # Apply an X gate to target states (each instance of "0")
    for state in target_states:
        for q_index, q_value in enumerate(state): #enumerate adds a counter to an iterable (such as list, tuple or string) and returns a enumerate object., the object returns (index,element)
            if q_value == '0':
                oracle.x((n-1)-q_index) #order is needs to be reversed, if "001" is target state, "1" is in index 2, but we want it to apply X gate on qubit in index 0
    
    #oracle.barrier()
    
    # Apply Multiple control X gate (using Toffoli gate an Hadamard gate)
    oracle.h(n-1)
    oracle.mcx(list(range(n-1)),(n-1))
    oracle.h(n-1)
    
    #oracle.barrier()
    
    # Apply an X gate to target states (each instance of "0")
    for state in target_states:
        for q_index, q_value in enumerate(state): #enumerate adds a counter to an iterable (such as list, tuple or string) and returns a enumerate object., the object returns (index,element)
            if q_value == '0':
                oracle.x((n-1)-q_index) #order is needs to be reversed, if "001" is target state, "1" is in index 2, but we want it to apply X gate on qubit in index 0
    
    oracle.to_gate()
    
    return oracle
        

def grover_diffuser(target_states):
    n = len(target_states[0]) 
    
    # Create quantum circuit for diffuser
    diffuser = QuantumCircuit(n,name="Diffuser")
    
    # Apply Hagamrd gates to all qubits
    diffuser.h(list(range(n)))
    
    # Apply X gate to all qubits
    diffuser.x(list(range(n)))
                
    #diffuser.barrier()
                
    # Apply Multiple control X gate (using Toffoli gate an Hadamard gate)
    diffuser.h(n-1)
    diffuser.mcx(list(range(n-1)),(n-1))
    diffuser.h(n-1)
       
    #diffuser.barrier()
    
     # Apply X gate to all qubits
    diffuser.x(list(range(n)))
                
    # Apply Hagamrd gates to all qubits
    diffuser.h(list(range(n)))
    
    diffuser.to_gate()
    
    return diffuser
                
def main(target_states):
    
    n = len(target_states[0])
    queries = math.ceil(math.sqrt(2**n)) 
    r = list(range(n))

    init = initialization(target_states)
    oracle = grover_oracle(target_states)
    diffuser = grover_diffuser(target_states)

    grover = QuantumCircuit(n,n)
    grover.append(init,r)
    
    print(f"Number of queries: {queries}")
    
    while queries > 0:
        grover.append(oracle,r)
        grover.append(diffuser,r)
        queries -= 1
        
    grover.measure(r,r)

    job = execute(grover,Aer.get_backend('qasm_simulator'),shots=1).result()
    counts = job.get_counts(grover)
    
    return plot_histogram(counts)

main(["100"])
    