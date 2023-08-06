
import numpy as np

from . import qfn

#### Basic Qubit States #####
#: Qubit with the state: :math:`\ket{0}`
QB0  = np.array([1,0])
#: Qubit with the state: :math:`\ket{1}`
QB1  = np.array([0,1])
#: Qubit with the state: :math:`\ket{00}`
QB00 = np.kron(QB0, QB0)
#: Qubit with the state: :math:`\ket{01}`
QB01 = np.kron(QB0, QB1)
#: Qubit with the state: :math:`\ket{10}`
QB10 = np.kron(QB1, QB0)
#: Qubit with the state: :math:`\ket{11}`
QB11 = np.kron(QB1, QB1)


##### Bell States #####
#: Bell state 00 :math:`\ket{\Phi^+} = \frac{1}{\sqrt2}(\ket{0_A} \otimes \ket{0_B} + \ket{1_A} \otimes \ket{1_B})`
BELL00 = 2**(-1/2)*qfn.state((0,0)) + 2**(-1/2)*qfn.state((1,1))
#: Bell state 00 :math:`\ket{\Phi^-} = \frac{1}{\sqrt2}(\ket{0_A} \otimes \ket{0_B} - \ket{1_A} \otimes \ket{1_B})`
BELL01 = 2**(-1/2)*qfn.state((0,1)) + 2**(-1/2)*qfn.state((1,0))
#: Bell state 00 :math:`\ket{\Psi^+} = \frac{1}{\sqrt2}(\ket{0_A} \otimes \ket{1_B} + \ket{1_A} \otimes \ket{0_B})`
BELL10 = 2**(-1/2)*qfn.state((0,0)) - 2**(-1/2)*qfn.state((1,1))
#: Bell state 00 :math:`\ket{\Psi^+} = \frac{1}{\sqrt2}(\ket{0_A} \otimes \ket{1_B} - \ket{1_A} \otimes \ket{0_B})`
BELL11 = 2**(-1/2)*qfn.state((0,1)) - 2**(-1/2)*qfn.state((1,0))
