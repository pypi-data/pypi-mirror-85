import numpy as np
import matplotlib.pyplot as plt
from neurodsp import filt, spectral, timefrequency
from scipy.signal import hilbert
import os, re, glob, pyopenephys
from matplotlib.ticker import MaxNLocator

def getSignals(dataLocation):
    '''
    '''
    file = pyopenephys.File(dataLocation) 
    experiments = file.experiments
    experiment=experiments[0]
    recordings=experiment.recordings
    recording=recordings[0]
    signals=recording.analog_signals[0].signal
    fs=int(recording.sample_rate)
    return fs, signals
def getAverages(dataLocation, method='mean', map='flat'):
    '''
    Gets averages of each channel and organizes it in a array by relative location on the shank.

    Parameters
    ----------
    method : string
        Put mean to return the means of all channels, and std first standard deviations. Defaults to mean.
    '''
    channelMap=[[5,4,6,3,7,2,8,1],[13,12,14,11,15,10,16,9],[21,20,22,19,23,18,24,17],[29,28,30,27,31,26,32,25]]# This map is organized by shank, and then by height on shank (e.g 5,13,21,29 being the lowest)
    channels=getChannels(dataLocation)
    if map=='flat':
        channelMap=np.arange(32)+1
        channelAverages=[]
        for i, x in enumerate(channelMap):
            if method=='mean':
                processedChannel=np.mean(channels[x-1]['data'])
            if method=='std':
                processedChannel=np.std(channels[x-1]['data'])
            channelAverages.append(processedChannel)
        return channelAverages
    else:
        shankAvgs=[]
        for i, x in enumerate(channelMap):
            channelAverages=[]
            for v in x:
                if method=='mean':
                    processedChannel=np.mean(channels[v-1]['data'])
                if method=='std':
                    processedChannel=np.std(channels[v-1]['data'])
                channelAverages.append(processedChannel)
            shankAvgs.append(np.array(channelAverages))
        return shankAvgs
def plotAverageSignal(dataLocation):
    fs, signals=getSignals(dataLocation)
    signals=signals.signal
    summatedSignal=np.array(np.zeros(len(signals[0])))
    for signal in signals:
        summatedSignal=summatedSignal+signal**2
    summatedSignal=(summatedSignal/len(signals))**(1/2)
    plt.plot(np.arange(len(summatedSignal)), summatedSignal)
def plotAverages(dataLocation, method='std'):
    channelMap=[5,4,6,3,7,2,8,1,13,12,14,11,15,10,16,9,21,20,22,19,23,18,24,17,29,28,30,27,31,26,32,25]# This map is organized by shank, and then by height on shank (e.g 5,13,21,29 being the lowest)
    averages=getAverages(dataLocation, method=method, map='')
    shank=averages[0]
    plt.scatter(channelMap[0:8],shank, label='Shank 1')
    shank=averages[1]
    plt.scatter(channelMap[8:16],shank, label='Shank 2')
    shank=averages[2]
    plt.scatter(channelMap[16:24],shank, label='Shank 3')
    shank=averages[3]
    plt.scatter(channelMap[24:32],shank, label='Shank 4')
    plt.legend()
    plt.xlabel('Channel Number')
    plt.ylabel(method.upper())
    plt.tight_layout()
def plotFiltered(dataLocation, r=[.1, 200]):
    file = pyopenephys.File(dataLocation) 
    experiments=file.experiments
    experiment=experiments[0]
    recordings=experiment.recordings
    recording=recordings[0]
    signals=recording.analog_signals[0]
    fs=int(recording.sample_rate)
    fc = (r[0], r[1])
    for x in range(32):
        sig=signals.signal[x]
        sig_filt = filt.filter_signal(sig, fs, 'bandpass', fc)
        plt.subplot(8,4,x+1)
        plt.plot(np.arange(len(sig_filt))/fs,sig_filt,label='Channel '+str(x+1))
        plt.ylim([-200,200])
        plt.xlim([58,80])
        plt.title('Channel '+str(x+1))
        plt.xlabel('Time (Seconds)')
        plt.tight_layout()
def plotHilbert(dataLocation, r=[.1, 200]):
    fs, signals=getSignals(dataLocation)
    fc = (r[0], r[1])
    for x in range(32):
        sig=signals.signal[x]
        sig_filt = filt.filter_signal(sig, fs, 'bandpass', fc)
        sig_hilbert = np.abs(timefrequency.hilbert.robust_hilbert(sig_filt, increase_n=True))
        plt.subplot(8,4,x+1)
        plt.plot(np.arange(len(sig_hilbert))/fs,sig_hilbert,label='Channel '+str(x+1))
        plt.ylim([0,300])
        plt.xlim([60,70])
        plt.title('Channel '+str(x+1))
        plt.xlabel('Time (Seconds)')
        plt.tight_layout()
def welchSignals(data, targetRange=range(32)):
    '''
    '''
    fs=data['fs']
    signals=data['signals']
    outputSignals=[]
    for x in targetRange:
        sig=signals.signal[x]
        freq_mean, psd_mean = spectral.compute_spectrum(sig, fs, nperseg=fs*2)
        outputSignals.append({'freq_mean': freq_mean, 'psd_mean': psd_mean})
    return outputSignals
def plotWelch(data, label, targetRange=range(32)):
    '''
    Plot a 4x32 array of welshed signals corresponding to each channel.
    '''
    signals=welchSignals(data, targetRange)
    for x in targetRange:
        signal=signals[x]
        freq_mean=signal['freq_mean']
        psd_mean=signal['psd_mean']
        plt.subplot(8,4,x+1)
        plt.loglog(freq_mean[:500], psd_mean[:500], label=label)
        plt.title('Channel '+str(x+1))
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Power')
        plt.tight_layout()
def plotSpectrograms(dataLocation):
    file = pyopenephys.File(dataLocation) 
    experiments=file.experiments
    experiment=experiments[0]
    recordings=experiment.recordings
    recording=recordings[0]
    signals=recording.analog_signals[0]
    signal=signals.signal[3]
    fs=int(recording.sample_rate)
    plt.figure(figsize=(15,20))
    for i in range(32):
        plt.subplot(8,4,i+1)
        data=signals.signal[i]
        plt.specgram(data,Fs=fs, NFFT=5*fs,mode='psd')
        plt.ylim(0,200)
        plt.xlabel('Time (seconds)')
        plt.ylabel('Hz')
    plt.tight_layout()
