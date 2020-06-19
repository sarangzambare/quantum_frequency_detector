from qiskit import QuantumCircuit, QuantumRegister, Aer, execute
from qiskit.visualization import plot_histogram, plot_state_city
from math import sqrt, pi, log
import numpy as np
import matplotlib.pyplot as plt



def plot_samples(samples):

    plt.plot(list(range(len(samples))), samples)


def get_fft_from_counts(counts, n_qubits):

    out = []
    keys = counts.keys()
    for i in range(2**n_qubits):
        id = get_bit_string(i, n_qubits)
        if(id in keys):
            out.append(counts[id])
        else:
            out.append(0)

    return out

def get_bit_string(n, n_qubits):
    """
    Returns the binary string of an integer with n_qubits characters
    """

    assert n < 2**n_qubits, 'n too big to binarise, increase n_qubits or decrease n'

    bs = "{0:b}".format(n)
    bs = "0"*(n_qubits - len(bs)) + bs

    return bs


def isPow2(x):
    return (x!=0) and (x & (x-1)) == 0

def getlog2(x):

    return (log(x)/log(2))


def normalize(samples):

    norm = np.linalg.norm(samples)

    return samples/norm, norm

def truncate_samples(samples, n_qubits):

    if(len(samples) <= 2**n_qubits):
        pass
    else:
        samples = samples[:2**n_qubits]
    return samples


def prepare_circuit(samples, normalize=True):

    """
    Args:
    amplitudes: List - A list of amplitudes with length equal to power of 2
    normalize: Bool - Optional flag to control normalization of samples, True by default
    Returns:
    circuit: QuantumCircuit - a quantum circuit initialized to the state given by amplitudes
    """


    num_amplitudes = len(samples)
    assert isPow2(num_amplitudes), 'len(amplitudes) should be power of 2'

    num_qubits = int(getlog2(num_amplitudes))
    q = QuantumRegister(num_qubits)
    qc = QuantumCircuit(q)

    if(normalize):
        ampls = samples / np.linalg.norm(samples)
    else:
        ampls = samples

    qc.initialize(ampls, [q[i] for i in range(num_qubits)])

    return qc
