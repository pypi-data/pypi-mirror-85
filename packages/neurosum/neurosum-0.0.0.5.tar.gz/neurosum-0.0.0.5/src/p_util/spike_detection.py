from neurodsp.filt.filter import filter_signal
import matlab.engine
import copy
import scipy.signal as signal
import numpy as np
def bin_sum(binned_channels):
    '''
    Sum spikes across bins to get the population spiking vectors
    '''
    summed_bins=[]
    #Equalize lengths of channel bins
    greatest_length=len(max(binned_channels, key=len))
    equal_channels=[]
    for channel in binned_channels:
        channel_difference=greatest_length-len(channel)
        equal_channels.append(np.append(channel, np.zeros(channel_difference).tolist()))
    #Sum up the bins
    for tbin in np.transpose(equal_channels):
        summed_bins.append(sum(tbin))
    return summed_bins
def bin_channels(channels, bin_length):
    '''
    Computes the bin function on a 64 channel electrode array
    '''
    bins=[] #bins each channel separately in the format of: channels[], bins{}, sums
    for channel in channels:
        bins.append(bin_channel(channel, bin_length))
    return bins
def bin_channel(spikes, bin_length):
    '''
    Put spike timings into bins
    '''
    bins = []
    if len(spikes)>0:
        # bin_floor is is the quantity of bins
        bin_floor = int(np.max(spikes)//bin_length)+1
        # Create an array of size bin_floor
        bins = np.zeros(bin_floor).tolist()
        # Iterate through the spikes, iterating the correct bin by one
        for spike in spikes:
            spikes_bin=int(spike//bin_length)
            bins[spikes_bin] += 1
    return bins
def wave_average(channels):
    '''
    Averages each channels average wave.
    '''
    average_wave=[]
    for channel in channels:
        average_wave.append(wave_averages(channel))
    average_wave=[x for x in average_wave if len(x)>0]
    return wave_averages(average_wave)
def wave_averages(waves_channel):
    '''
    It takes in the product of one channel from the function collect_spikes() and produce a single average spike waveform
    '''
    average_wave=[]
    for twave in np.transpose(waves_channel):
        average_wave.append(np.mean(twave))
    return average_wave

def collect_spikes(data, well, window_length):
    '''
    data: is the time series data organized in channels, amplitudes. 
    Will return an empty array even if there are spikes if all window lengths are out of bounds
    location: is the spike time locations, organized in a 2d array of channels, locations.
    window_length: A tuple of how much on each side of the spike to collect. Both values are positive. 0 index being how much on the left the spike
    '''
    channels=[]
    waveforms=[]
    for ichannel, channel in  enumerate(well):
        for ispike, spike in enumerate(channel):
            try:
                waveforms.append(np.transpose(data[ichannel][int(spike-window_length):int(spike+window_length)]))
            except IndexError:
                pass
                # print('Spike window: %d outside data range' % spike)
        channels.append(waveforms)

    # For some reason, some waveforms our length 0. This is a fix.
    waveforms = [waveform for waveform in waveforms if len(waveform) == window_length*2]
    return  waveforms

def detect_spikes(data, fs, standard_threshold=5, matlab_engine = None):
    '''
    Detecting spikes using basic algorithm.
    Returns a list of  channels(list) x spike_times(list). 
    '''
    
    minimum_peak_distance=np.ceil(.002*fs)
    minimum_peak_distance=1
    number_channels=len(data)
    spikes=[None]*number_channels

    for channel in range(0, number_channels):
        # Make the threshold
        threshold=np.median(np.abs(data[channel])/.6745)*standard_threshold
        # Quick check if anything goes over the thresh to avoid heavy calcs 
        max_value = np.amax(np.abs(data[channel]))
        if max_value > threshold:
            # Form matlab compatable data
            m_channel = matlab.double(data[channel].tolist())
            # Do the spike finding
            _, spikes[channel] = matlab_engine.findpeaks(m_channel, 'minpeakheight', float(threshold), 'minpeakdistance', float(minimum_peak_distance), nargout=2)
            # Fix Matlab return type weirdness
            spikes[channel] = np.asarray(spikes[channel]).tolist()
            if type(spikes[channel]) is float:
                spikes[channel] = [spikes[channel]]
            else:
                spikes[channel] = spikes[channel][0]
            print('\t%s spikes found on channel %s\r'%(len(spikes[channel]),channel), end = '', flush = False)
        else:
            spikes[channel]=[]
            print('\t0 spikes found on channel %s\r'%(channel,), end = '', flush = False)
    return spikes
