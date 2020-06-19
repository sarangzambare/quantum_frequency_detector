from tools.qft import qft, inverse_qft
from pydub.generators import Sine
from pydub import AudioSegment
from pydub.playback import play
from tools.audio_tools import prepare_circuit_from_audiosegment, prepare_circuit_from_samples, prepare_circuit
%config InlineBackend.figure_format = 'svg'
from qiskit import Aer, execute, QuantumCircuit, IBMQ
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from tools.tools import get_bit_string, get_fft_from_counts, plot_samples
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack

from qiskit.providers.ibmq import least_busy
from qiskit.tools.monitor import job_monitor
from math import sqrt, pi


IBMQ.load_account()
provider = IBMQ.get_provider(hub='ibm-q')


n_qubits = 3
n_samples = 2**n_qubits
audio = AudioSegment.from_file('900hz.wav')
audio.set_frame_rate(2000)
frame_rate = audio.frame_rate #2000
samples = audio.get_array_of_samples()[:n_samples]
plt.xlabel('sample_num')
plt.ylabel('value')
plt.plot(list(range(len(samples))), samples)


qcs = prepare_circuit_from_samples(samples, n_qubits)
qft(qcs, n_qubits)
qcs.measure_all()

qasm_backend = Aer.get_backend('qasm_simulator')
real_backend = least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= 5
                                       and not x.configuration().simulator
                                       and x.status().operational==True))


#substitute with the desired backend
out = execute(qcs, qasm_backend, shots=8192).result()
counts = out.get_counts()
fft = get_fft_from_counts(counts, n_qubits)[:n_samples//2]


plt.xlabel('sample_num')
plt.ylabel('value')
plt.plot(list(range(len(fft[:]))), fft[:])
plt.savefig('./html/blog/assets/f_8.png', dpi=150, bbox_inches='tight')

top_indices = np.argsort(-np.array(fft))
freqs = top_indices*frame_rate/n_samples
# get top 5 detected frequencies
print(freqs[:5])
