from pydub import AudioSegment
from pydub.playback import play
from pydub.generators import Sine
import os
from tools.tools import prepare_circuit, truncate_samples, normalize
from tools.qft import qft



def get_frequencies_from_fft(fft, frame_rate, n=5):
    """
    Returns top n loudest frequencies in fft
    """

    N = len(fft)
    T = 1.0/frame_rate

    fstep = (1/(2.0*T))/((N//2)-1)



    yf = fft[:N//2]
    indexes = np.argsort(yf)
    freqs = indexes*fstep

    return freqs[:n]


def get_audio_samples(segment, n_qubits):
    """
    get the first 2^num_qubits samples from the given audio segment
    """

    samples = segment.get_array_of_samples()
    assert len(samples) >= 2**n_qubits, 'Audio segment too short'

    return samples[:2**n_qubits]


def prepare_circuit_from_audiosegment(segment, n_qubits):
    """
    Prepares a quantum circuit with n_qubits initialized with a quantum state corresponding
    to the samples from the audio segment
    """

    samples = get_audio_samples(segment, n_qubits)
    qc = prepare_circuit(samples)

    return qc

def prepare_circuit_from_samples(samples, n_qubits):
    """
    Prepares a quantum circuit with n_qubits initialized with a quantum state corresponding
    to the samples provided
    """

    samples = truncate_samples(samples, n_qubits)
    qc = prepare_circuit(samples)

    return qc
