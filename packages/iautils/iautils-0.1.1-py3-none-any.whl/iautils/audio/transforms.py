import numpy as np
import librosa, cv2
from scipy import signal
from functools import partial
from .external import PyOctaveBand


################################################################################################################################
#### RECIPES (Combination of Transformations)
################################################################################################################################

################################################################
#### RecipeMel
################################################################
class RecipeMel(object):
    '''
    1. 동일한 hop length와 서로 다른 3개의 n_fft를 갖는 mel spectrograms을 구하여 image 형식 (heigth x width x 3 ch, 8 bit depth)의 array 생성
    2. image 형식의 array를 augment (image와 동일하게 처리) 
      (1) square crop (width만 crop하여 square image를 구함)
      (2) roll
      (3) flip
    
    return
      3d numpy array (height x width x channel)
    
    init. arguments
      height: default is 224 pixel (= number of frequency bins) to use ImageNet CNN models.
      hop_sec: default 0.01 sec (= 10 ms), hop_length = sampling rate * hop_sec
      n_fft_factors: n_fft_factor * hop_length = n_fft
    '''
    def __init__(self, height=224, hop_sec=0.01, fft_secs=[0.08, 0.08, 0.08]):
        self.specs = []
        for fft_sec in fft_secs:
            self.specs.append(MelSpectrogram(height=height, hop_sec=hop_sec, fft_sec=fft_sec))
        
    def __call__(self, y, sr, augment=False):
        '''
        input
          y [numpy array], sr [int]
          
        return
          S [dB]
        '''
        # Stack Channels
        channels = []
        for spec in self.specs:
            S = spec(y, sr)
            S = ((S-S.min())/(S.max()-S.min()) * 255).astype(np.int)
            channels.append(S)
        x = np.stack(channels, -1)        
        
        # Augmentation
        if augment:
            x = SquareCrop('random')(x)
            x = Roll()(x)
            x = Flip()(x)
        else:
            x = SquareCrop('left')(x)
        
        return x

################################################################
#### RecipeSTFT ~ multi layer
################################################################
class RecipeSTFT(object):
    '''
    1. 동일한 hop length와 서로 다른 3개의 n_fft를 갖는 STFT를 구하여 image 형식 (heigth x width x 3 ch, 8 bit depth)의 array 생성
    2. image 형식의 array를 augment (image와 동일하게 처리) 
      (1) square crop (width만 crop하여 square image를 구함)
      (2) roll
      (3) flip
    
    return 
      3d numpy array (height x width x channel).
    
    init. arguments
      height: default is 224 pixel (= number of frequency bins)
      hop_sec: default 0.01 sec (= 10 ms), hop_length = sampling rate * hop_sec
      n_fft_factors: n_fft_factor * hop_length = n_fft
    '''
    def __init__(self, height=224, hop_sec=0.01, fft_secs=[0.08, 0.16, 0.32]):
        self.specs = []
        for fft_sec in fft_secs:
            self.specs.append(STFT(height=height, hop_sec=hop_sec, fft_sec=fft_sec))
        
    def __call__(self, y, sr, augment=False):
        '''
        input
          y [numpy array], sr [int]
          
        return
          S [dB]
        '''
        # Stack STFT spec.
        channels = []
        for spec in self.specs:
            S = spec(y, sr)
            S = ((S-S.min())/(S.max()-S.min()) * 255).astype(np.int)
            channels.append(S)
        x = np.stack(channels, -1)
        
        # Augmentation
        if augment:
            x = SquareCrop('random')(x)
            x = Roll()(x)
            x = Flip()(x)
        else:
            x = SquareCrop('left')(x)
        
        return x


################################################################################################################################
#### SPECTROGRAM & RTA
################################################################################################################################

################################################################
#### Octave band filter
################################################################
class OctaveBandFilter(object):
    '''
    Octave band filter
    
    init.
    :param sr:
    :param fraction: bandwidth 'b', 1/3-octave b=3, 2/3-octave b=3/2, 1-octave b=1 (default 3)
    :param order:
    :param limits: 
    
    call
    :param y: y
    :param sr: sampling rate
    
    return 
    spl[dB]
    '''
    def __init__(self, sr=None, fraction=3, order=6, fmin=12, fmax=12800):
        
        # estimate sr if sr not specified
        self.sr = sr if sr else fmax * 2
        self.fraction = fraction
        self.order = order
        self.fmin = fmin
        self.fmax = fmax
        
        # generate frequencies & remove outer frequency
        freq_arr = PyOctaveBand.getansifrequencies(self.fraction, self.fmin, self.fmax)
        idx = np.where(freq_arr[:, 2] > self.sr / 2)
        if any(idx[0]):
            freq_arr = np.delete(freq_arr, idx, axis=0)
        self.freqs = freq_arr[:, 0]
        self.freq_limits = freq_arr[:, 1:]
        self.N = self.freqs.shape[0]
        
        # Calculate the downsampling factor (array of integers with size [freq])   
        guard = 0.10
        factor = np.floor((self.sr / (2 + guard)) / self.freq_limits[:, 1])
        factor = np.clip(factor, 1, 50).astype('int')
        self.factor = factor
        
        # Get SOS filter coefficients (3d array w/ shape (freq, order, 6))
        butter = partial(signal.butter, self.order, btype='bandpass', output='sos')
        wns = self.freq_limits / (self.sr / self.factor /2).reshape(-1, 1)
        sos = np.apply_along_axis(butter, 1, wns)
        self.sos = sos
        
    def __call__(self, x, sr):
        
        if sr != self.sr:
            print(f"WARNING: input sr ({sr}) is not equal to initiated sr ({self.sr}), instance is reinitiated w/ sr {sr}")
            self.__init__(sr, self.fraction, self.order, self.fmin, self.fmax)
            
        spl = np.zeros(self.N)
            
        for idx in range(self.N):
            y = signal.decimate(x, self.factor[idx])
            y = signal.sosfilt(self.sos[idx], y)
            y = np.std(y)
            spl[idx] = 20 * np.log10(y / 2e-5)
        
        return spl


################################################################
#### Mel Spectrogram
################################################################
class MelSpectrogram(object):
    '''
    librosa.feature.melspectrogram을 height, hop_sec에 대해 다시 작성한 것
    
    return 
      2d numpy array, unit dB
    
    init. arguments
      height: default is 224 pixel (= number of frequency bins)
      hop_sec: default 0.01 sec (= 10 ms), hop_length = sampling rate * hop_sec    
    '''
    def __init__(self, height=224, hop_sec=0.01, fft_sec=0.08):
        self.height = height
        self.hop_sec = hop_sec
        self.fft_sec = fft_sec
    
    def __call__(self, y, sr):
        hop_length = int(sr * self.hop_sec)
        n_fft = int(sr * self.fft_sec)
        S = librosa.feature.melspectrogram(y, sr, n_fft=n_fft, hop_length=hop_length, n_mels=self.height)
        S = librosa.power_to_db(S)
        
        return S
    
################################################################
#### STFT
################################################################
class STFT(object):
    '''
    librosa.STFT를 height, hop_sec에 대해 다시 작성한 것
    
    return 
      2d numpy array, unit dB
    
    init. arguments
      height: default is 224 pixel (= number of frequency bins) 
      hop_sec: default 0.01 sec (= 10 ms), hop_length = sampling rate * hop_sec
      
    example
      get_stft = STFT()
      S = get_stft(y, sr)
    '''
    def __init__(self, height=224, hop_sec=0.01, fft_sec=0.08):
        self.height = height
        self.hop_sec = hop_sec
        self.fft_sec = fft_sec
        cv2.setNumThreads(0)
        
    def __call__(self, y, sr):
        '''
        input
          y [numpy array], sr [int]
          
        return
          S [dB]
        '''
        hop_length = int(sr * self.hop_sec)
        n_fft = int(sr * self.fft_sec)
        S = librosa.stft(y, n_fft, hop_length, )
        S = np.abs(S)
        S = librosa.amplitude_to_db(S)
        S = cv2.resize(S, (S.shape[1], self.height))
        
        return S

    
################################################################
#### DWT
################################################################



################################################################
#### CWT
################################################################



################################################################
#### Scale
################################################################
# 0 ~ 1 float
# 0 ~ 255 uint8
class FreqStandardization(object):
    '''
    Frequency Standardization (Mean, std are required)
    
    init arguments
      mean, std
      
    return
      input
    '''
    def __init__(self, mean=None, std=None, cutoff=(-3, 3)):
        self.mean = mean
        self.std = std
        self.cutoff = cutoff
        
    def __call__(self, y, sr):
        '''
        input
          y [numpy array], sr [int]
          
        return
          S [dB]
        '''
        if all([x is not None for x in [self.mean, self.std]]):
            y = (y - self.mean) / self.std
            cutL, cutH = self.cutoff
            y = np.clip(y, cutL, cutH)
            y = (y - cutL) / (cutH - cutL) 
        else:
            print("mean, std are required!")
        return y, sr


################################################################################################################################
# IMAGE TRANSFORMATION (Crop, Flip, Rolling, ...)
################################################################################################################################

################################################################
#### Square Crop
################################################################
class ToImage(object):
    '''
    Spectrogram stack하여 이미지로 변환, 8 bit로 convert
    (추가할 것 ~ normalize, standardize)
    '''
    def __init__(self):
        pass
    
    def __call__(self, channels:list):
        img = []
        for ch in channels:
            # normalize 방법에 따라 바뀔 수 있도록 할 것
            ch = ((ch-ch.min())/(ch.max()-ch.min()) * 255).astype(np.int)
            img.append(ch)           
        return np.stack(img, -1)

################################################################
#### Square Crop
################################################################
class SquareCrop(object):   
    '''
    모든 변환은 Channel Last 기준 (h x w x c), pytorch에서 사용하려면 (c x h )
    '''
    def __init__(self, position='left'):
        self.position = position
    
    def __call__(self, x):
        '''
        input
          2d numpy array w/ shape (h x w)
          
        return
          2d numpy array w/ shape (h x h)
        '''
        h, w, c = x.shape
            
        #### if width is smaller than height, drop the data 
        if w <= h:
            return x

        #### do crop
        if self.position == 'left':
            x = x[:, :h, :]
        elif self.position == 'center': 
            x = x[:, w//2-h//2:w//2+h//2, :]
        elif self.position == 'right':
            x = x[:, -h:, :]
        elif self.position == 'random':
            l = np.random.randint(0, w - h)
            x = x[:, l:l+h, :]
        else:
            print('ERROR!!! crop options: [left, center, right, random]')  
                
        return x

################################################################
#### Resize
################################################################
class Resize(object):
    '''
    모든 변환은 Channel Last 기준 (HWC)
    '''
    def __init__(self, height=224, width='fixed_aspect'):
        self.height = height
        self.width = width
        cv2.setNumThreads(0)
        
    def __call__(self, x):
        
        #### REORDER
        h, w, c = x.shape
        
        #### SET WIDTH
        if self.width == 'fixed_aspect':
            width = int(w * self.height / h)
        elif self.width == 'fixed_width':
            width = w
        elif type(width) is int:
            width = width
        else:
            print('ERROR!!! resize options: "fixed_aspect", "fixed_width", int()')
        
        #### RESIZE
        x = cv2.resize(x, (width, self.height))
        
        return x
    
################################################################
#### Rolling
################################################################
class Roll(object):
    '''
    모든 변환은 Channel Last 기준 (HWC)
    '''
    def __init__(self, shift='random', freq=0.3):
        self.shift = shift
        self.freq = freq
    
    def __call__(self, x):
        
        if np.random.random() < self.freq:
            
            #### Get Order
            axis = 1   # H: 0, W: 1, C: 2
            width = x.shape[axis]
            
            #### ROLL
            if self.shift == 'random':
                shift = np.random.randint(0, width)
            elif type(self.shift) is int:
                shift = self.shift
            else:
                print("ERROR!!! only 'random' and integer are available now")
            x = np.roll(x, shift, axis)
            
        return x
        
################################################################
#### Flip
################################################################
class Flip(object):
    '''
    모든 변환은 Channel Last 기준 (HWC)
    '''
    def __init__(self, freq=0.3):
        self.freq = freq
    
    def __call__(self, x):
        
        if np.random.random() < self.freq:
            #### Flip (mirror)
            x = cv2.flip(x, 1)

        return x
