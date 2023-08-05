# Copyright (c) 2020. Jose M. Requena-Plens
# Woojin Modified 2020/11/09
"""
Octave-Band and Fractional Octave-Band filter.
"""

import numpy as np
from functools import partial
from scipy import signal
import matplotlib.pyplot as plt

# Public methods
__all__ = ['octavefilter', 'getansifrequencies', 'normalizedfreq']


def octavefilter(x, sr=None, fraction=1, order=6, fmin=12, fmax=12600, show=False):
    """
    Filter a signal with octave or fractional octave filter bank. This
    method uses a Butterworth filter with Second-Order Sections
    coefficients. To obtain the correct coefficients, a subsampling is
    applied to the signal in each filtered band.

    :param x: Signal
    :param fs: Sample rate
    :param fraction: Bandwidth 'b'. Examples: 1/3-octave b=3, 1-octave b=1,
    2/3-octave b = 3/2. [Optional] Default: 1.
    :param order: Order of Butterworth filter. [Optional] Default: 6.
    :param limits: Minimum and maximum limit frequencies. [Optional] Default
    [12,20000]
    :param show: Boolean for plot o not the filter response.
    :returns: Sound Pressure Level and Frequency array
    """

    # use estimated sr
    if not sr:
        sr = fmax * 2
    
    # Generate frequencies
    # freq[:, 0]: represent freq
    # freq[:, 1]: freq lower bound
    # freq[:, 2]: freq upper bound
    freq = getansifrequencies(fraction, fmin, fmax)

    # Remove outer frequency to prevent filter error (fs/2 < freq), freq[2] == freq_upper
    idx = np.where(freq[:, 2] > sr / 2)
    if any(idx[0]):
        print('*********\nLow sampling rate, frequencies above fs/2 will be removed\n*********')
        freq = np.delete(freq, idx, axis=0)        
    N = freq.shape[0]

    # Calculate the downsampling factor (array of integers with size [freq])   
    guard = 0.10
    factor = np.floor((sr / (2 + guard)) / freq[:, 2])
    factor = np.clip(factor, 1, 50)
    factor = factor.astype('int')

    # Get SOS filter coefficients (3D - matrix with size: [freq,order,6])
    butter = partial(signal.butter, 6, btype='bandpass', output='sos')
    wns = freq[:, 1:] / (sr / factor /2).reshape(-1, 1)
    sos = np.apply_along_axis(butter, 1, wns)
    
    # Show filter
    if show:
        _showfilter(sos, freq, freq_u, freq_d, sr, factor)
    
    # Create array with SPL for each frequency band
    spl = np.zeros(N)
    
    for idx in range(N):
        y = signal.decimate(x, factor[idx])
        y = signal.sosfilt(sos[idx], y)
        y = np.std(y)
        spl[idx] = 20 * np.log10(y / 2e-5)
    
    return spl, freq[:,0]


def _showfilter(sos, freq, freq_u, freq_d, fs, factor):
    wn = 8192
    w = np.zeros([wn, len(freq)])
    h = np.zeros([wn, len(freq)], dtype=np.complex_)

    for idx in range(len(freq)):
        fsd = fs / factor[idx]  # New sampling rate
        w[:, idx], h[:, idx] = signal.sosfreqz(
            sos[idx],
            worN=wn,
            whole=False,
            fs=fsd)

    fig, ax = plt.subplots()
    ax.semilogx(w, 20 * np.log10(abs(h) + np.finfo(float).eps), 'b')
    ax.grid(which='major')
    ax.grid(which='minor', linestyle=':')
    ax.set_xlabel(r'Frequency [Hz]')
    ax.set_ylabel('Amplitude [dB]')
    ax.set_title('Second-Order Sections - Butterworth Filter')
    plt.xlim(freq_d[0] * 0.8, freq_u[-1] * 1.2)
    plt.ylim(-4, 1)
    ax.set_xticks([16, 31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000])
    ax.set_xticklabels(['16', '31.5', '63', '125', '250', '500',
                        '1k', '2k', '4k', '8k', '16k'])
    plt.show()

    
def getansifrequencies(fraction, fmin=12, fmax=12600):
    """ ANSI s1.11-2004 && IEC 61260-1-2014
    Array of frequencies and its edges according to the ANSI and IEC standard.

    :param fraction: Bandwidth 'b'. Examples: 1/3-octave b=3, 1-octave b=1,
    2/3-octave b = 3/2
    :param limits: It is a list with the minimum and maximum frequency that
    the array should have. Example: [12,20000]
    :returns: Frequency array, lower edge array and upper edge array
    :rtype: list, list, list
    """

    # :fmin, fmax: limits
    # :g         : Octave ratio (ANSI s1.11, 3.2, pg. 2)
    # :fr        : Reference frequency (ANSI s1.11, 3.4, pg. 2)
    # :ber       : Band-edge ratio (ANSI s1.11, 3.7, pg. 3)
    g = 10 ** (3 / 10) 
    fr = 1000
    ber = g ** (1 / (2 * fraction))

    # ratio for ODD or EVEN ('x' solve from ANSI s1.11, eq. 3 ~ ODD or eq. 4 ~ EVEN)
    (A, B) = (1, 30) if fraction % 2 else (2, 59)
    ratio = lambda x: g ** ((A * x - B) / (A * fraction))
        
    # Get starting index 'x' and first center frequency    
    x = np.round((A * fraction * np.log(fmin/fr) + B * np.log(g)) / (A * np.log(g)))
    freq = ratio(x) * fr
    
    # Get each frequency until reach maximum frequency
    freq_latest = 0    
    # Increase index - get new frequency - append 
    while freq_latest * ber < fmax:
        x = x + 1
        freq_latest = ratio(x) * fr
        freq = np.append(freq, freq_latest)

    # return (center) freq[:, 0], (lower) freq[:, 1], (upper) freq[:, 2]
    return np.stack([freq, freq / ber, freq * ber], axis=1)


def normalizedfreq(fraction):
    """
    Normalized frequencies for one-octave and third-octave band. [IEC
    61260-1-2014]

    :param fraction: Octave type, for one octave fraction=1,
    for third-octave fraction=3
    :type fraction: int
    :returns: frequencies array
    :rtype: list
    """
    predefined = {
        1: np.array([16, 31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]),
        3: np.array([12.5, 16, 20, 25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200, 
                     250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 
                     3150, 4000, 5000, 6300, 8000, 10000, 12500, 16000, 20000]),
    }
    
    return predefined[fraction]