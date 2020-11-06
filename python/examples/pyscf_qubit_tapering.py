from qcor import *

# Create the H2 hamiltonian with Pyscf
H = createOperator('pyscf', {'basis': 'sto-3g', 'geometry': 'H  0.000000   0.0      0.0\nH   0.0        0.0  .7474'})
print('\nOriginal:\n', H.toString())

# Run the Qubit Tapering Observable Transform
H_tapered = operatorTransform('qubit-tapering', H)
print('\nTapered:\n', H_tapered)

# Define a simple 1 qubit ansatz
@qjit
def ansatz(q : qreg, x : List[float]):
    Rx(q[0], x[0])
    Ry(q[0], x[1])

# Create the problem model, provide the state 
# prep circuit, Hamiltonian and note variational parameters 
num_params = 2
problemModel = qsim.ModelBuilder.createModel(ansatz, H_tapered, 2)

# Create the VQE workflow
workflow = qsim.getWorkflow('vqe')

# Execute and print the result
result = workflow.execute(problemModel)
energy = result['energy']
print(energy)