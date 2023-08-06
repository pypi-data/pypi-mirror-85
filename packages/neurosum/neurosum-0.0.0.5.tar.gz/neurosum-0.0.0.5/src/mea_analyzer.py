from fooof import FOOOFGroup, FOOOF
from os import path
import matlab.engine
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import sys, os, scipy.io, pickle, h5py, argparse, glob, time
from pathlib import Path
from src.p_util.old_util import getSignals
import src.config as config
import src.p_util.preprocessing as pre
import src.p_util.spike_detection as sd
from statsmodels.tsa.stattools import acf
from neurodsp.spectral.power import compute_spectrum_welch as welch
from neurodsp.plts.spectral import plot_power_spectra as plot_psd
from neurodsp.plts.time_series import plot_time_series as plot_ts
import importlib.util
from scipy import signal
import configparser

class mea_wrapper:
    def __init__(self, user_todo=[1,1,1,1,1,1,1,1,1], settings_file=None, dir_name = None, mea_shape = (3,4)):
        self.mea_shape = mea_shape
        self.directory = dir_name
        self.setup_matlab()
        self._import_constants(settings_file)
        # Figure parameters
        self.fig_x = (35, 15)
        self.float_precision = 'float16'
        # Dependency set up
        self.func_list = [self.lp_well, self.hp_well, self.calculate_psd, 
                self.detect_spike, self.calculate_psv, self.autocor_psv, 
                self.calculate_psv_traces, self.get_spike_waveforms, self.calculate_psd_psv]
        self.pfunc_list = [None, None, self.plot_psds,
                self.plot_raster, self.plot_psv, self.plot_autocor,
                self.plot_psv_traces, self.plot_waveforms, self.plot_psd_psv]
        self.func_names = ['lp','hp','psd',
                'ss','psv','psdpsv',
                'apsv','psvw','sw']
        d_matrix = np.array([
                    [1,0,0,0,0,0,0,0,0], # Low pass 
                    [0,1,0,0,0,0,0,0,0], # Hi pass
                    [1,0,1,0,0,0,0,0,0], # PSD
                    [0,1,0,1,0,0,0,0,0], # Spike sort
                    [0,1,0,1,1,0,0,0,0], # PSV
                    [0,1,0,1,1,1,0,0,0], # Autocorrelation of PSV
                    [0,1,0,1,1,1,1,0,0], # PSV waveforms
                    [0,1,0,1,0,0,0,1,0],  # Spike waveforms
                    [0,1,0,1,1,0,0,0,1]  # PSD of PSV
                    ])

        self.to_do = np.dot(user_todo, d_matrix)
        print(self.to_do)
        # Initialize file specific variables
        self.low_pass_well      = []
        self.high_pass_well     = []
        self.psds               = []
        self.spike_wells        = []
        self.psvs               = []
        self.smooth_psvs        = []
        self.waveforms          = []
        self.psv_traces_wells   = []
        self.psd_psvs           = []
        self.data_list = [self.low_pass_well, self.high_pass_well, self.psds, 
                self.spike_wells, self.psvs, self.smooth_psvs, 
                self.waveforms, self.psv_traces_wells, self.psd_psvs]
        
    def raw_summary(self, raw_file, raw_dec=None):
        '''
        Calculates the summary statistics of a Axis raw file.
        '''
        if raw_dec==None:
            # Extract useful information from the path
            self.dir_name   = raw_file.split('.')[0].split('(')[0]
            self.plate_name = self.dir_name.split('/')[-2]
            self.date       = self.dir_name.split('/')[-3]
            self.filter     = self.dir_name.split('/')[-1]
        else:
            self.dir_name, self.plate_name, self.date, self.filter = raw_dec(raw_file)     

        # Create locations for where we save things
        self.create_plot_locs()
        print(self.to_do)
        # Loading the data if it exists
        for i, (do, loc, data) in enumerate(zip(self.to_do, self.save_locs, self.data_list)):
            if do:
                try:
                     data = np.load(loc, allow_pickle=True)
                     self.to_do[i] = 0
                except IOError:
                    pass
        print(self.to_do)
        # Figure out what file we are given, and converted to Python readable 
        if os.path.isfile(self.dir_name):
            pass
        else:
            p_print('Converting to HDF5(.mat)...')
            self.eng.MEA_convert(raw_file, self.dir_name, matlab.double((np.arange(12)+1).tolist()), nargout=0)
        self.config['wells_to_analyze'] = str(len(glob.glob(f'{self.dir_name}/**.mat')))
        # Well by well analysis
        self.make_directory()
        for self.well_index in range(self.config.getint('wells_to_analyze')):
#            self.find_analyses()
            if self.to_do[0] or self.to_do[1]:
                self.load_well()
            for (analysis_name, do, function) in zip(self.func_names, self.to_do, self.func_list):
                if do:
                    function()
                else:
                    p_print(f'Skipping {analysis_name}...')
                    time.sleep(1)
        # Saving
#        self.save_spikes()
        for (do, loc, data) in zip(self.to_do, self.save_locs, self.data_list):
            if do:
                self.default_save(loc, data)
        # Plots
        for (do, function) in zip(self.to_do, self.pfunc_list):
            if do and function is not None:
                function()
        p_print('The summary statistics have finished computing. See output folder.')
        time.sleep(2)
        plt.close('all')
        self.eng.close()
        p_print('')

    def remove_analysis(self, a):
        if type(a) == str:
            self.to_do[self.func_names.index(a)] = 0
        else:
            self.to_do[a] = 0
    def find_analyses(self):
        # Find existing analyses that have been saved somewhere
        if path.exists(f'{self.low_loc}/well{self.well_index}.np'):
            self.load_low_pass_well(self.well_index)
            self.remove_analysis('lp')
        if path.exists(f'{self.high_loc}/well{self.well_index}.np'):
            self.load_high_pass_well(self.well_index)
            self.remove_analysis('hp')
        # Load spikes
        if path.exists(self.spikes_loc):
            if len(self.spike_wells) < 1:
                p_print('Loaded spike file...')
                self.load_spikes()
                self.remove_analysis('ss')


    '''
    -------------------------------
    Plotting
    -------------------------------
    '''
    def plot_fooof(self):
        '''
        '''
        plt.figure(10)
        fig, axs  = self.get_axis()
        p_print(np.array(self.fooof_recordings).T.shape)
#        for ax, well in zip(axs, self.psds):
#            ax.plot(well)
#        plot_name = 'fooof_intercept'
#        plt.savefig(f'{self.output_directory}/{plot_name}.png')
    def plot_psds(self):
        '''
        '''
        plt.figure(2)
        fig, axs  = self.get_axis()
        for ax, well in zip(axs, self.psds):
            for channel in well:
                plot_psd(self.psd_freqs[0], channel, ax=ax)
        mpl.rcParams['lines.linewidth'] = .1
        plt.savefig(self.welch_plot_loc)
        mpl.rcParams['lines.linewidth'] = 1
    def plot_raster(self):
        '''
        '''
        plt.figure(2)
        fig, axs  = self.get_axis()
        fig.suptitle('Spike Raster')
        for ax, well in zip(axs, self.spike_wells):
            ax.eventplot([[spike/self.config.getint('fs') for spike in channel] for channel in well])
#            ax.set_title('Spike Raster', fontsize=self.config.getint('titleSize'))
            ax.set_ylabel('Channel number', fontsize=self.config.getint('labelSize'))
            ax.set_xlabel('Time (s)', fontsize=self.config.getint('labelSize'))
        plt.savefig(self.raster_plot_loc)

    def plot_waveforms(self):
        # Set up plots
        plt.figure(6)
        fig, axs  = self.get_axis()
        fig.suptitle('Spike Waveforms')
        # Create the X array
        self.wave_t_ms=np.arange(self.config.getint('wave_size')*2)/self.config.getint('fs')*1000
        for ax, well in zip(axs, self.waveforms):
            if len(well) > 0:
                wave_average=np.mean(well, axis = 0)
                [ax.plot(self.wave_t_ms, waveform, linewidth = .08) for waveform in well]
                ax.plot(self.wave_t_ms, wave_average, linewidth=2, color='red')
    #            ax.set_title('Spike Waveforms', fontsize=self.config.getint('titleSize'))
                ax.set_ylabel('Amplitude', fontsize=self.config.getint('labelSize'))
                ax.set_xlabel('Time (ms)', fontsize=self.config.getint('labelSize'))
        # Save plot
        plt.savefig(self.traces_plot_loc)

    def plot_autocor(self):
        plt.figure(5)
        fig, axs  = self.get_axis()
        fig.suptitle('Autocorrelation of PSV')

        for ax, x_auto, y_auto in zip(axs, self.x_autos, self.y_autos):
            '''
            Get autocorrelation for the population spiking vector
            '''
            ax.plot(np.array(x_auto)*(self.config.getint('bin_length')/self.config.getint('fs')), (np.array(y_auto)/max(y_auto)))
#            ax.set_title('Autocorrelation of PSV', fontsize=self.config.getint('titleSize'))
            ax.set_ylabel('Autocorrelation', fontsize=self.config.getint('labelSize'))
            ax.set_xlabel('Shifts (s)', fontsize=self.config.getint('labelSize'))
        plt.savefig(self.autocor_plot_loc)

    def plot_psv(self):
        plt.figure(4)
        fig, axs  = self.get_axis()
        fig.suptitle('Population Spiking Vector (PSV)')
        for ax, psv in zip(axs, self.psvs):
            t_psv = np.arange(len(psv))*(self.config.getint('bin_length')/self.config.getint('fs'))
            ax.plot(t_psv, psv)
#            ax.set_title('Population Spiking Vector (PSV)', fontsize=15)
            ax.set_ylabel('Bins', fontsize=12)
            ax.set_xlabel('Time (s)', fontsize=12)
        plt.savefig(self.psv_plot_loc)

    def plot_psd_psv(self):
        plt.figure(7)
        fig, axs  = self.get_axis()
        for ax, (psv_freq, psv_power) in zip(axs, self.psd_psvs):
            # Get the power spectral distribution for the population spiking vector
            ax.set_title('PSD of PSV', fontsize=self.config.getint('titleSize'))
            plot_psd(psv_freq, psv_power, ax=ax)
        plt.savefig(self.psvpsd_plot_loc)

    def plot_psv_traces(self):
        p_print('\tPlotting PSV Traces...')
        trace_low   = 2
        trace_high = 2
        bin_length = self.config.getint('fs')//1000 # 1ms
        plt.figure(7)
        fig, axs  = self.get_axis()
        for i, (ax, well) in enumerate(zip(axs, self.psv_traces)):
            x_array = False
            for trace in well:
                if not type(x_array) == type(np.array([])):
                    x_array = np.arange(len(trace))-bin_length//trace_low
                ax.plot(x_array, trace, linewidth=.2)
            if len(well) > 0:
                lens=[len(trace) for trace in well]
                avg_trace = np.mean(well, axis=0)
                ax.plot(x_array, avg_trace, linewidth=3, color='red')
        plt.savefig(self.psvtraces_plot_loc)
    
    '''
    -------------------------------
    Calculation Functions
    -------------------------------
    '''
    def calculate_fooof(self):
        for (freqs, powers) in zip(self.psd_freqs, self.psds):
            self.fooof.fit(freqs, powers)
            self.fooof_wells.append(self.fooof.get_params('aperiodic_params'))

    def autocor_psv(self):
        p_print('Auto Correlating the psv')
        self.y_autos = []
        self.x_autos = []
        for psv in self.psvs:
            '''
            Get autocorrelation for the population spiking vector
            '''
            psv_length=len(psv)
            y_auto=acf_sm = acf(psv, nlags=self.config.getint('acf_lags'), fft=True)
            x_auto=np.arange(len(y_auto))
            self.y_autos.append(y_auto)
            self.x_autos.append(x_auto)

    def calculate_psd_psv(self):
        '''
        Get the power spectral distribution for the population spiking vector
        Create variable 'psd_psv', a tuple of (frequencies, powers)
        '''
        p_print('Getting the psd of the psv...')
        for psv in self.psvs:
            self.psd_psvs.append(welch(np.array(psv), self.config.getint('fs')/self.config.getint('bin_length'), nperseg=self.config.getint('spike_nperseg'), noverlap=self.config.getint('spike_nperseg')//2))

    def calculate_psv(self):
        '''
        Get population spiking vector from a wells Spike data(channel x loc of Spike)
        '''
        p_print('Getting psv...')
        bins=sd.bin_channels(self.spike_wells[self.well_index], self.config.getint('bin_length'))
        # Append the well psv to the one of the wells
        self.psvs.append(sd.bin_sum(bins))
        self.smooth_psvs.append(signal.convolve(self.psvs[-1], signal.windows.gaussian(50, .01)))

    def calculate_psv_traces(self):
        p_print('Getting psv traces...')
        bin_length = self.config.getint('fs')//1000 # 1ms
        trace_low   = 2
        trace_high = 2
        self.psv_traces = [] # wells x traces x psv_spike
        spike_shapes = []
        for peak in signal.find_peaks(self.smooth_psvs[-1], height=self.config.getint('psv_spike_height'))[0]:
            low = peak-bin_length//trace_low
            high = peak+bin_length*trace_high
            if high <= len(well) and low >= 0:
                spike_shapes.append(well[low:high])
            else:
                p_print('trace frogoten!!!')
        self.psv_traces.append(spike_shapes)

    def lp_well(self):
        p_print('Applying a low pass filter...')
        self.low_pass_well = pre.low_pass_filter(self.referenced_well, self.config.getint('fs'), low_filter=self.config.getint('ds_fs'))
#        self.save_low_pass_well()
    def hp_well(self):
        p_print('Applying a high pass filter...')
        self.high_pass_well = pre.high_pass_filter(self.referenced_well, self.config.getint('fs'))
#        self.save_high_pass_well()
        self.referenced_well = None

    def calculate_psd(self):
        '''
        '''
        p_print('Computing psd...')
        # wellxchannelxpsd(powers)
        self.psd_freqs = []
        power_list=[]
        median = np.median(self.low_pass_well, axis = 0)
        well_psds = []
        for channel in self.low_pass_well:
            well_psds.append(welch(channel, self.config.getint('ds_fs'), nperseg=self.config.getint('nperseg'), noverlap=self.config.getint('noverlap'))[1])
        ch_freq, ch_power = welch(median, self.config.getint('ds_fs'), nperseg=self.config.getint('nperseg'), noverlap=self.config.getint('noverlap'))
            
        # Get the median first value of our psd list
        mfv = np.median(np.array(well_psds).T[0])
        # Filter out values that are well above the median
        well_psds = [psd for psd in well_psds if not psd[0] > 2*mfv]
        self.psd_freqs.append(ch_freq)
        self.psds.append(well_psds)

    def detect_spike(self):
        '''
        Detect spikes for only one well
        '''
        p_print('Sorting spikes...')
        self.spike_analysis = False
        # Check if a spikes file exists, and if it does use that
        spikes = sd.detect_spikes(self.high_pass_well, self.config.getint('fs'), standard_threshold=self.config.getfloat('spike_threshold'), matlab_engine = self.eng)
        self.spike_wells.append(spikes)

    def get_spike_waveforms(self):
        # Append current well waveforms
        t_ms=self.config.getint('fs')*1000
        self.waveforms.append(sd.collect_spikes(self.high_pass_well, self.spike_wells[self.well_index], self.config.getint('wave_size')))

    def get_waveform_t(self):
        self.wave_t_ms = []
        for channel in self.waveforms:
            for waveform in channel:
                if len(self.wave_t_ms) < 0:
                    self.wave_t_ms=np.arange(len(waveform))/t_ms
    def reference_well(self):
        #Re- reference the timeseries.
        p_print('Re-referencing...')
        self.referenced_well = pre.reference_channels(self.raw_well)
        
    def create_t_series(self):
        #Make down sampled/low-pass filtered time array.
#        self.low_pass_t = np.arange(len(self.low_pass_wells[0][0]))/self.config.getint('ds_fs')
        self.low_pass_t = np.arange(len(self.low_pass_well[0]))/self.config.getint('ds_fs')

        #Make high-pass filter time array.
        self.high_pass_t = np.arange(len(self.high_pass_well[0]))/self.config.getint('fs')

    # Memory Management
    # --------------------------------------------------------------- 
    def load_well(self):
        self.well = [] # array of wells x channels x time series
        p_print('Loading data from folder...')
        filename = '%s/well_%s.mat' % (self.dir_name, self.well_index+1)
        self.raw_well = np.array(h5py.File(filename, 'r')['MEA'])
        if self.config.getint('wells_to_analyze') > len(self.raw_well):
            p_print('Inputted well amount is too high, using the max instead...')
            self.config['wells_to_analyze'] = len(self.raw_well)
        self.reference_well()
    def load_wells(self):
        self.wells = [] # array of wells x channels x time series
        p_print('loading data from folder...')
        for x in range(self.config.getint('wells_to_analyze')):
            filename = '%s/well_%s.mat' % (self.dir_name, x+1)
            self.wells.append(h5py.file(filename, 'r')['mea'])
        self.wells = np.array(self.wells, dtype = self.float_precision)
    def make_directory(self):
        try:
            # Create target Directory
            os.mkdir(self.output_directory.split('/')[0])
            p_print(f'Directory {self.output_directory} Created')
        except FileExistsError:
            p_print(f'Directory {self.output_directory} already exists')
        try:
            # Create target Directory
            os.mkdir(self.output_directory.split('/')[1])
            p_print(f'Directory {self.output_directory} Created')
        except FileExistsError:
            p_print(f'Directory {self.output_directory} already exists')

    def del_wells(self):
        del self.wells
    def del_low_pass_wells(self):
        del self.low_pass_wells
    def del_referenced_wells(self):
        del self.referenced_wells
    def load_low_pass_well(self, well):
        self.low_pass_well = np.load('%s/well%i.np'%(self.low_loc, well))
    def load_low_pass_wells(self):
        self.low_pass_wells = [np.load('%s/%s/well%i.np'%(self.output_directory, self.low_loc, well)) for well in range(self.config.getint('wells_to_analyze'))]
    def load_high_pass_well(self, well):
        self.high_pass_well = np.load('%s/well%i.np'%(self.high_loc, well))
    def load_high_pass_wells(self):
        self.high_pass_wells = [np.load('%s/%s/well%i.np'%(self.output_directory, self.high_loc, well)) for well in range(self.config.getint('wells_to_analyze'))]
    def save_fooof_wells(self):
        with open(self.fooof_loc, 'wb') as f:
            np.save(f, well)
    def save_high_pass_well(self):
        os.makedirs(self.high_loc, exist_ok=True)
        with open('%s/well%i.np'%(self.high_loc, self.well_index), 'wb') as f:
            np.save(f, self.high_pass_well)
    def save_low_pass_well(self):
        os.makedirs(self.low_loc, exist_ok=True)
        with open('%s/well%i.np'%(self.low_loc, self.well_index), 'wb') as f:
            np.save(f, self.low_pass_well)
    def load_psds(self):
        self.psds = np.load(self.psds_loc).tolist()
    def save_psds(self):
        with open(self.psd_loc, 'wb') as f:
            np.save(f, np.array(self.psds))
    def load_spikes(self):
        self.spike_wells = np.load(self.spikes_loc, allow_pickle=True).tolist()
    def save_spikes(self):
        with open(self.spikes_loc, 'wb') as f:
            np.save(f, np.array(self.spike_wells, dtype=object))
    def default_save(self, loc,  data):
        with open(loc, 'wb') as f:
            np.save(f, np.array(data, dtype=object))
    def create_plot_locs(self):
        # Set up file locations
        self.output_directory = f'processed/{self.plate_name}'

        self.data_dir       = f'{self.output_directory}/{self.filter}/{self.date}'
        self.low_loc        = f'{self.data_dir}/low_pass.np'
        self.high_loc       = f'{self.data_dir}/high_pass.np'
        self.psds_loc       = f'{self.data_dir}/psds.np'
        self.spikes_loc     = f'{self.data_dir}/spikes.np'
        self.psv_loc        = f'{self.data_dir}/psv.np'
        self.psvpsd_loc     = f'{self.data_dir}/psvpsd.np'
        self.psvtraces_loc  = f'{self.data_dir}/psvtraces.np'
        self.traces_loc     = f'{self.data_dir}/traces.np'
        self.autocor_loc    = f'{self.data_dir}/autocor.np'
        self.save_locs = [self.low_loc, self.high_loc, self.psds_loc, 
                self.spikes_loc, self.psv_loc, self.autocor_loc,
                self.psvtraces_loc, self.traces_loc, self.psvpsd_loc]
        # For plots
        plots_loc = f'{self.output_directory}/plots'
        Path(plots_loc).mkdir(parents=True, exist_ok=True)
        self.welch_plot_loc     = f'{plots_loc}/welch_{self.filter}_{self.date}'
        self.raster_plot_loc    = f'{plots_loc}/spikeraster_{self.filter}_{self.date}'
        self.psv_plot_loc       = f'{plots_loc}/psv_{self.filter}_{self.date}'
        self.psvpsd_plot_loc    = f'{plots_loc}/psdpsv_{self.filter}_{self.date}'
        self.traces_plot_loc    = f'{plots_loc}/traces_{self.filter}_{self.date}'
        self.psvtraces_plot_loc = f'{plots_loc}/psvtraces_{self.filter}_{self.date}'
        self.autocor_plot_loc   = f'{plots_loc}/autocor_{self.filter}_{self.date}'
        self.plot_locs = [None, None, self.welch_plot_loc, 
                self.raster_plot_loc, self.psv_plot_loc, self.autocor_plot_loc, 
                self.psvtraces_plot_loc, self.traces_plot_loc, self.psvpsd_plot_loc]

    def get_axis(self):
        # Make subplots, and return the axes in a flat list
        fig, axs = plt.subplots(self.mea_shape[0], self.mea_shape[1], figsize=(self.config.getint('figsizex'), self.config.getint('figsizey')))
        axs = np.concatenate(axs).ravel()
        return fig, axs

    def _import_constants(self, sf):
        if sf:
            path=sf
        else:
            path='config.ini'
        self.config = configparser.ConfigParser()
        self.config['default'] = {
            'fs' : '12500', # Sample rate of both original signal, and high past signal
            'ds_fs' : '1000', # Sample Rate Of Down Sampled signal.
            'wells_to_analyze' : '6', # Number of wells
            'figsizex' : '35',
            'figsizey' : '15',
            'labelSize' : '18',
            'titleSize' : '20',
            'spike_threshold' : '5.5',  #Scaler threshold for what is considered a spike based on standard deviation
            'bin_length' : '13', #Convention to do one millisecond
            'nperseg' : '1000', #Segment length of psd welch function for low passed data
            'noverlap' : '500', #Overlap of psd welch function for low passed data
            'spike_nperseg' : '12500',
            'spike_noverlap' : '6250',
            'wave_size' : '20',
            'acf_lags' : '10000',
            'psv_spike_height' : '2',
#            'lp' : ''
        }
        if os.path.isdir(path):
            p_print(f'Loading {path} in your working directory...')
            self.config.read(path)
        else:
            p_print('Using the default config...')
        self.config = self.config['default'] 

    def setup_matlab(self):
        self.eng = matlab.engine.start_matlab()
        self.eng.addpath(os.path.dirname(os.path.abspath(__file__))+'/functions',nargout=0)
        self.eng.addpath(os.path.dirname(os.path.abspath(__file__))+'/Axion',nargout=0)
def p_print(s):
    # A print used for progress notifications
    print(f'\t{s.ljust(65)}', end='\r', flush=True)

