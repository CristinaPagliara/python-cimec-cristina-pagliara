# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 2024

@author: Cristina Pagliara
"""
import numpy as np
from scipy import signal
from scipy.signal import find_peaks, filtfilt, hilbert, butter

#%%
def preprocess_photometrydata(fs,raw_data, freqRange,window=15):
    '''
    Parameters  # LP: you could have at least filled the automatically generated docstring ;)
    ----------
    fs : TYPE
        DESCRIPTION.
    raw_data : TYPE
        DESCRIPTION.
    freqRange : TYPE
        DESCRIPTION.
        
    Returns
    -------
    freq_pks_data : TYPE
        DESCRIPTION.
    '''
    
    freq, power_spectrum = signal.welch(raw_data, window='hann', fs=fs, nperseg=fs*30, detrend='constant', return_onesided=True, scaling='density', axis=-1, average='mean')
    
    
    # LP comments!
    indices = np.where((freq > freqRange[0])&(freq < freqRange[1]))
    power_spectrum_data=power_spectrum[indices[0]]
    freq_data=freq[indices[0]]
    
    pks_data, properties= find_peaks(power_spectrum_data,height=1e5, distance=50) 
     
    freq_pks_data = freq_data[pks_data]
    
    range_freq_data=[freq_pks_data[0]-window,freq_pks_data[0]+window]
    nyquist = 0.5 * fs
    normalized_range_freq_data = [range_freq_data[0] / nyquist, range_freq_data[1] / nyquist]
    b, a = butter(4, normalized_range_freq_data, btype='band')
    filtered_data = filtfilt(b, a, raw_data)
    
    amplitude_data = hilbert(filtered_data)
    amplitude_envelope = np.abs(amplitude_data)
    

    return amplitude_envelope