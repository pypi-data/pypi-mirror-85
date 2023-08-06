import os, re, glob, pyopenephys
import pdb; 

from scipy.signal import resample_poly
from neurodsp.filt import filter_signal
import numpy as np
from fractions import gcd

def reference_channels(well, average='mean'):
    '''
    This function does two things:
        Leave out any channels where all values are zero(Indicating broken electrode).
        Subtract each channels average from itself element wise.
    '''
    return  np.array([channel for channel in well if not np.all(channel == 0)]) - np.median(well, axis = 0)
def low_pass_filter(data, fs, low_filter=1000):
    low_pass, data =  resample_channel(data[-1], fs), data[:-1]
    for channel in data:
        low_pass = np.vstack([low_pass, resample_channel(channel, fs)])
    return low_pass.astype('float16')
def high_pass_filter(data, fs, hi_filter=(300, 3000)):
    hi_pass, data = filter_signal(data[-1], fs, 'bandpass', hi_filter, remove_edges=False), data[:-1]
    for channel in data:
        hi_pass = np.vstack([hi_pass, filter_signal(channel, fs, 'bandpass', hi_filter, remove_edges=False)])
    return hi_pass.astype('float16')

def resample_channel(channel, fs, mea_filter=1000):
    '''
    Resample lfp, first by upsampling then, downsampling. This is done to handle fractional down sample factors.
    '''
    up_sample_frequency=(mea_filter*fs)//gcd(mea_filter, fs)
    up_sample_factor=up_sample_frequency/fs
    down_sample_factor=up_sample_frequency/mea_filter
        
    return resample_poly(channel, up_sample_factor,  down_sample_factor)
    
def getSignals(dataLocation):
    '''
    From file location return data in a neater package.
    '''
    file = pyopenephys.File(dataLocation) 
    experiments=file.experiments
    experiment=experiments[0]
    recordings=experiment.recordings
    recording=recordings[0]
    channels=recording.analog_signals[0].signal
    fs=int(recording.sample_rate)
    data={'fs':fs,'channels':channels}
    return data
