import librosa
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import librosa.display


def audio_process(songname: str, mono: bool = True, duration: int = 30) -> pd.DataFrame:
    """
    :return: DataFrame of all the features
    :rtype: Pandas DataFrame
    :param mono: Specify whether mono is True or False It defaults to True
    :param songname: Specify the filename to process
    :param duration: Specify the duration of the file
    """

    y, sr = librosa.load(songname, mono=mono, duration=duration)

    rmse = librosa.feature.rms(y=y)
    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
    spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
    spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    zcr = librosa.feature.zero_crossing_rate(y)
    mfcc = librosa.feature.mfcc(y=y, sr=sr)

    lis = {
        "chroma_stft": [np.mean(chroma_stft)],
        "rmse": [np.mean(rmse)],
        "spectral_centroid": [np.mean(spec_cent)],
        "spectral_bandwidth": [np.mean(spec_bw)],
        "rolloff": [np.mean(rolloff)],
        "zero_crossing_rate": [np.mean(zcr)]
    }

    for i, e in enumerate(mfcc):
        lis[f'mfcc{i + 1}'] = [np.mean(e)]

    return pd.DataFrame(lis)


def spectrogram_plot(audio_file: str, mono: bool = True, duration: int = 5):
    """

    :rtype: Plot
    """
    y, sr = librosa.load(audio_file, mono=mono, duration=duration)
    plot = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=13)
    plot = librosa.power_to_db(plot, ref=np.max)
    librosa.display.specshow(plot, y_axis='mel', x_axis='time')
    plt.title('Mel-frequency spectrogram')
    plt.colorbar()
    plt.tight_layout()
    plt.show()
