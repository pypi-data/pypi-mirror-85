import os, textwrap, random
from pathlib import Path
import pandas as pd
import numpy as np
import librosa, cv2, soundfile
from tqdm import tqdm
from nptdms import TdmsFile


################################################################
# make labels inferred from subdirs
################################################################
# def make_filelist(filepath, exts=["wav", "tdms"]):
#     '''
#     fast: 하위 1 level의 폴더만 탐색함, (예) filepath/NG, filepath/OK, ...
#     '''
    
#     subdirs = [Path(d) for d in os.scandir(filepath) if os.path.isdir(d)]
    
#     files = []
#     for subdir in subdirs:
#         for ext in exts:
#             files.extend(subdir.glob(f"**/*.{ext.lstrip('.')}"))
        
#     filelist = pd.DataFrame({
#         'filename': [f.name for f in files],
#         'filepath': [str(f) for f in files],
#     })
    
#     return filelist


################################################################
# make labels inferred from subdirs
################################################################
def make_labels(filepath, exts=["wav", "tdms"], fast=True):
    '''
    fast: 하위 1 level의 폴더만 탐색함, (예) filepath/NG, filepath/OK, ...
    '''
    
    subdirs = [Path(d) for d in os.scandir(filepath) if os.path.isdir(d)]
    
    files = []
    for subdir in subdirs:
        for ext in exts:
            if fast:
                files.extend(subdir.glob(f"*.{ext.lstrip('.')}"))
            else:
                files.extend(subdir.glob(f"**/*.{ext.lstrip('.')}"))
        
    labels = pd.DataFrame({
        'filename': [f.name for f in files],
        'filepath': [str(f) for f in files],
        'label': [f.parent.name for f in files]
    })
    
    return labels

################################################################
# extract tdms
################################################################
def extract_tdms(list_filepath):
    # placeholder
    extracted = {
        'group': [],
    }
    
    for filepath in list_filepath:
        f = TdmsFile(filepath)

        # file can have one or more groups
        for g in f.groups():

            # 1. update group name
            g_name = g.name
            extracted['group'].append(g_name)

            # 2. update group properties
            g_props = {k: v for k, v in g.properties.items()}
            for k, v in g_props.items():
                key = 'gr_' + k
                if key not in extracted.keys():
                    extracted[key] = [] 
                extracted[key].append(v)

            # group can have one or more channels
            for ch in g.channels():

                # 3. update channel value
                if ch.name not in extracted.keys():
                    extracted[ch.name] = []
                extracted[ch.name].append(ch[:])

                # 4. update channel properties
                ch_props = {k2: v2 for k2, v2 in ch.properties.items()}
                for k, v in ch_props.items():
                    key = ch.name + '_' + k
                    if key not in extracted.keys():
                        extracted[key] = []
                    extracted[key].append(v)

    extracted = pd.DataFrame(extracted)
        
    return extracted


################################################################
# slice dataframe 
################################################################
def estimate_parquet_size(func, input_, n_samples=100, **kwargs):
    
    TEMP_FILENAME = 'parquet_size_check.parquet'
    
    if type(input_) is not list:
        input_ = list(input_)
    n_total = len(input_)
    samples = random.sample(input_, n_samples)
    
    output = func(samples, **kwargs)
    if type(output) is not pd.DataFrame:
        output = pd.DataFrame(output)
    output.to_parquet(TEMP_FILENAME)
    
    sample_size_mb = os.path.getsize(TEMP_FILENAME)/1024/1024
    required_memory_gb = output.memory_usage(index=True, deep=True).sum()/n_samples*n_total/1024/1024
    n_rows_per_parquet = int(1024 / sample_size_mb * n_samples)
    
    os.remove(TEMP_FILENAME)
    
    print(f"#### Parquet Size Estimation ####")
    print(f" - write 1 parquet per {n_rows_per_parquet} rows (for 1 GB/parquet)")
    print(f" - if you load all {n_total} rows at once, {required_memory_gb:.0f} GB will be required")
    
    return n_rows_per_parquet, required_memory_gb


################################################################
# slice dataframe 
################################################################
def slice_df(df, chunk_size=None, n_chunks=None):
    '''
    input
    :df: dataframe
    :chunk_size: 
    :n_chunks:
    
    return
    dict(i:padded_string, chunk:dataframe)
    '''
    
    len_df = len(df)
    
    if n_chunks and not chunk_size:
        chunk_size = np.ceil(len_df / n_chunks).astype(int)
    if chunk_size and not n_chunks:
        n_chunks = np.ceil(len_df / chunk_size).astype(int)
    else:
        print("set a parameter between chunk_size and n_chunks")
        return None
    
    n_zfill = np.trunc(np.log10(n_chunks)).astype(int) + 1
    
    return {f"{str(i+1).zfill(n_zfill)}": df[i*chunk_size:(i+1)*chunk_size].reset_index(drop=True) for i in np.arange(0, n_chunks)}


################################################################
# encode labels
################################################################
def encode_labels(labels, reverse=True, verbose=True):
    '''
    (NG, OK) become (1, 0) if reverse else (0, 1)
    (NG1, NG2, NG3, OK) becomes (3, 2, 1, 0) if reverse else (0, 1, 2, 3)
    '''
    names = sorted(labels['label'].unique(), reverse=reverse)
    encoder = {name: code for code, name in enumerate(names)}
    decoder = {code: name for code, name in enumerate(names)}
    
    labels_encoded = labels.copy()
    labels_encoded['label'] = [encoder[x] for x in labels['label']]
    
    if verbose:
        print(f'<LABELS> {len(names)} classes')
        print(f'encoder = {encoder}')
        print(f'decoder = {decoder}')
        print('')
        
    return labels_encoded, encoder, decoder


################################################################
# encode labels
################################################################

# 아래 def와 무관하게, 왜 global df labels의 값이 바뀌는지 확인...
def one_hot_encode_labels(labels, class_nothing='nothing', reverse=True, verbose=True):
    '''
    binary cross entropy 사용을 위한 one_hot_encoding
    class_nothing class 지정하면 해당 class는 (0, 0, ..., 0) 값을 가짐 (예를 들어 OK를 OK으로 분류하는 것이 아니라 아무것도 아님으로 분류)
    '''
    names = sorted(set('|'.join(labels['label'].tolist()).split('|')), reverse=reverse)
    if class_nothing in names:
        names.remove(class_nothing)
    n_classes = len(names)
    encoder = {name: code for code, name in enumerate(names)}
    decoder = {code: name for code, name in enumerate(names)}
    
    #### one hot encoding
    labels_encoded = labels.copy()
    for i in labels_encoded.index:
        label_vector = n_classes * [0]
        classes = labels_encoded.at[i, 'label'].split('|')
        if class_nothing in classes:
            classes.remove(class_nothing)
        for c in classes:
            label_vector[encoder[c]] = 1
        labels_encoded.at[i, 'label'] = '|'.join([str(e) for e in label_vector])
    
    if verbose:
        print(f'<LABELS> {n_classes} classes')
        print(f'encoder = {encoder}')
        print(f'decoder = {decoder}')
        print('')
        
    return labels_encoded, encoder, decoder


################################################################
# load_tmds
################################################################
# def load_tdms(filepath, sr_new=None, channel='CPsignal1'):
#     try:
#         ch = TdmsFile(filepath).groups()[0][channel]
#         y = ch[:]
#         sr = 1//ch.properties['dt']
#     except Exception as ex:
#         print('ERROR!!! {ex}')
#         return None, None
#     return y, sr

################################################################
# load_file
################################################################
def load(filepath, group=None, channel=None, sr=None):
    ext = filepath.rsplit('.', 1)[-1]
    
    # wav
    if ext == 'wav':
        y, sr = soundfile.read(filepath, samplerate=sr)
        return y, sr
    
    # tdms
    elif ext == 'tdms':
        # read group
        f = TdmsFile(filepath)
        if group is not None:
            try:
                g = f[group]
            except:
                print(f"There is no group name '{group}'. Available groups are:")
                for g in f.groups():
                    print(g.name, end=", ")
                return
        else:
            if len(f.groups()) == 1:
                g = f.groups()[0]
            else:
                print(f"You have multiple groups. Please select one:")
                for g in f.groups():
                    print(g.name, end=", ")
                return

        # read channel
        try:
            ch = g[channel]
            y = ch[:]
        except:
            print(f"Channel '{channel}' is not exist. Available channels are:")
            for ch in g.channels():
                print(ch.name, end=", ")
            return
        
        # read properties 'dt'
        try:
            sr = int(1/ch.properties['dt'])
        except Exception as ex:
            if ex == 'dt':
                print(f"sampling rate will be None because the channel '{channel}' has no property name 'dt'. please set sampling rate manually")
            else:
                print(ex)
            sr = None
            
        return y, sr
        
################################################################
# make_confusion_matrix
################################################################
def make_confusion_matrix(truth, predict):
    cm = pd.crosstab(truth, predict)
    for l in cm.index:
        if l not in cm.columns:
            cm[l] = 0
    return cm[cm.index]

        
################################################################
#### AudioDataset (DEFAULT)
################################################################
class AudioDataset(object):
    
    def __init__(self, labels, prep, label_dtype=None):
        
        # pd.series to list
        self.filename = labels.filename.tolist()
        self.filepath = labels.filepath.tolist()
        
        # assume binery_cross_entropy if label's codes are object (string), bce requires float32 label
        if labels.label.dtype == object:
            self.label = labels.label.str.split('|', expand=True).astype(int).to_numpy()
            self.dtype = np.float32
        # assume cross_entropy if label's codes are integer, cross_entropy requires int64 label
        else:
            self.label = labels.label.tolist()
            self.dtype = np.int64
        
        # prep = load + transforms
        self.prep = prep

        # manual dtype
        if label_dtype:
            self.dtype = label_dtype
    
    def __len__(self):
        return len(self.label)
    
    def __getitem__(self, idx):
        
        # parse index
#         idx = idx.tolist() if torch.is_tensor(idx) else idx
        
        # get filename, filepath, y
        filename = self.filename[idx]
        filepath = self.filepath[idx]
#         y = torch.tensor(self.label[idx], dtype=self.dtype)
        y = self.dtype(self.label[idx])
        
        # prep: filepath -> load -> transform -> model input x
        x = self.prep(filepath)
        
        return x, y, filename
