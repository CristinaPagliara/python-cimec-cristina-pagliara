# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 2024

@author: Cristina Pagliara
"""
from matplotlib import pyplot as plt
from pathlib import Path

from nwb_conv.import_utils.fiberphotometry import import_edr
from preprocess_photometrydata import preprocess_photometrydata 

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
# LP: comments!
fs= 1. / header['DT']

photometry_signal=preprocess_photometrydata(fs,raw_data[:,params['rawSignal']], params['freqRangeSignal'],window=15)

photometry_control=preprocess_photometrydata(fs,raw_data[:,params['rawControl']], params['freqRangeControl'],window=15)

f, ax = plt.subplots(2, 1)

ax[0].plot(photometry_signal, c="C1")
plt.rc('axes.spines', bottom=True, left=True, right=False, top=False)
ax[0].set(xlabel="Something", ylabel="Something else")

ax[1].plot(photometry_control)
plt.rc('axes.spines', bottom=True, left=True, right=False, top=False)
ax[1].set(xlabel="Something", ylabel="Something else")


