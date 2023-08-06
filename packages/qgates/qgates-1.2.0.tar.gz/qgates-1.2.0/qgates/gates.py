
import numpy as np

from . import qfn

### Defining some traditional gates
#: 2x2 identity gate :math:`\begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}`
IDEN = np.array([
    [1,0],
    [0,1]])
#: 2x2 logical NOT gate :math:`\begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}`
NOT = np.array([
    [0,1],
    [1,0]])
#: 2x4 logical OR gate :math:`\begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 1 & 1 \end{bmatrix}`
OR = np.array([
    [1,0,0,0],
    [0,1,1,1]])
#: 2x4 logical AND gate :math:`\begin{bmatrix} 1 & 1 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}`
AND = np.array([
    [1,1,1,0],
    [0,0,0,1]])
#: 2x4 logical XOR gate :math:`\begin{bmatrix} 1 & 0 & 0 & 1 \\ 0 & 1 & 1 & 0 \end{bmatrix}`
XOR = np.array([
    [1,0,0,1],
    [0,1,1,0]])
#: 2x4 logical NOR gate :math:`\begin{bmatrix} 0 & 1 & 1 & 1 \\ 1 & 0 & 0 & 0 \end{bmatrix}`
NOR  = NOT @ OR
#: 2x4 logical NAND gate :math:`\begin{bmatrix} 0 & 0 & 0 & 1 \\ 1 & 1 & 1 & 0 \end{bmatrix}`
NAND = NOT @ AND
#: 4x2 COPY gate :math:`\begin{bmatrix} 1 & 0 \\ 0 & 0 \\ 0 & 0 \\ 0 & 1 \end{bmatrix}`
COPY = np.array([
    [1,0],
    [0,0],
    [0,0],
    [0,1]])
#: 4x4 SWAP gate :math:`\begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}`
SWAP = np.array([
    [1,0,0,0],
    [0,0,1,0],
    [0,1,0,0],
    [0,0,0,1]])


### Defining some quantum gates
#: 4x4 Quantum CNOT gate: :math:`\begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \end{bmatrix}`
CNOT = np.kron(IDEN,XOR) @ np.kron(COPY,IDEN)
#: 8x8 Quantum TOFFOLI gate: :math:`\begin{bmatrix} 1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 \\ 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 \end{bmatrix}`
TOFFOLI = (
    np.kron(np.kron(IDEN,IDEN),XOR) @
    np.kron(np.kron(np.kron(IDEN,IDEN),AND),IDEN) @
    np.kron(np.kron(np.kron(IDEN,SWAP),IDEN),IDEN) @
    np.kron(np.kron(COPY,COPY),IDEN)
    )
#: 2x2 Quantum HADAMARD gate :math:`\begin{bmatrix} \frac{1}{\sqrt{2}} && \frac{1}{\sqrt{2}} \\ \frac{1}{\sqrt{2}} && \frac{-1}{\sqrt{2}} \end{bmatrix}`
HAD = np.array([[1,1],[1,-1]]) * np.exp2(-1/2)
