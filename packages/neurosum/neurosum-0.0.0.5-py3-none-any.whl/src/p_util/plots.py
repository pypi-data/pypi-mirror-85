import matplotlib.pyplot as plt
import neurodsp.spectral.power.compute_spectrum as computer_spectrum
def plotAll(signal, spikes):
    compute_spectrum(signal)
    plt.eventplot(spikes)
