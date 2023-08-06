# AudioFeaturizer

AudioFeaturizer is a python package that uses librosa under the hood and extracts features from audio and returns it into a pandas dataframe. 
It also has a spectrogram generation function which generates spectrogram of the audio file path which is passed. 


## Installation

You can install the AudioFeaturizer from [PyPI](https://pypi.org/project/AudioFeaturizer/):

    pip install AudioFeaturizer

The reader is supported on Python 3.7 and above.


## How to Use

For Extracting Features from single file
```
>>> from AudioFeaturizer.audio_featurizer import *
>>> audio_process(r'D:\PYTHON_FILES\audio-ml\genres\classical\classical.00000.wav')
   chroma_stft      rmse  spectral_centroid  spectral_bandwidth  ...    mfcc17    mfcc18    mfcc19    mfcc20
0     0.252391  0.036255        1505.299012         1558.952849  ... -0.303796  1.778557  0.890328 -0.837884

[1 rows x 26 columns]
>>>
```

For Displaying Spectrogram
```
from AudioFeaturizer.audio_featurizer import *

spectrogram_plot(r'D:\PYTHON_FILES\audio-ml\genres\classical\classical.00000.wav')
```


For Processing a list of files
```
In[0]: from AudioFeaturizer.audio_featurizer import audio_process_list
       audio_process_list([r"D:\PYTHON_FILES\audio classification\Man Out Of Town.wav",
                           r"D:\PYTHON_FILES\audio classification\Trumpet Tune.wav"])
    
Out[0]: 
   chroma_stft      rmse  spectral_centroid  ...    mfcc18    mfcc19    mfcc20
0     0.407153  0.201064        2507.575812  ... -2.347450 -5.120735  3.309853
1     0.276051  0.030480        1467.355071  ... -2.594764 -4.458375  1.309751
[2 rows x 26 columns]

```