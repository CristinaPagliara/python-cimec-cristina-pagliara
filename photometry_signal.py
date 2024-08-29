# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 10:23:44 2024

@author: Cristina Pagliara
"""
import numpy as np
from matplotlib import pyplot as plt
from pathlib import Path
from nwb_conv.import_utils.fiberphotometry import import_edr

from scipy.signal import find_peaks, filtfilt, hilbert
from scipy import signal
from scipy.signal import butter

#%%
def preprocess_photometrydata(fs,raw_data, freqRange,window=15):
    '''
    Parameters
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

# %%
data_folder = Path(
    r"C:\Users\cristina.pagliara\code\python-cimec-cristina-pagliara\data"
)

edr_file = list((data_folder / "photometry").glob("*.EDR"))[0]

params = {
    'freqRangeSignal': [208, 228],
    'freqRangeControl': [310, 330],
    'rawSignal': 5,
    'rawControl': 6,
}

raw_data, header = import_edr(str(edr_file))

#%%
fs= 1. / header['DT']

photometry_signal=preprocess_photometrydata(fs,raw_data[:,params['rawSignal']], params['freqRangeSignal'],window=15)

photometry_control=preprocess_photometrydata(fs,raw_data[:,params['rawControl']], params['freqRangeControl'],window=15)

plt.plot(photometry_signal)
plt.plot(photometry_control)
