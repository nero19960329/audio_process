import numpy as np
from pyaudio import PyAudio, paInt16
import wave
import configs
import matplotlib.pyplot as plt

def read_wave_file(fileName):
    f = wave.open(fileName, "rb")
    params = f.getparams()
    #print params[:4]
    pa = PyAudio()
    stream = pa.open(format = pa.get_format_from_width(f.getsampwidth()), channels = f.getnchannels(), rate = f.getframerate(), output = True)
    full_data = ""
    data = f.readframes(configs.NUM_SAMPLES)

    while data:
        full_data += data
        data = f.readframes(data)

    return full_data

def seperate(fileName):
    data = read_wave_file(fileName)
    wave_data = np.fromstring(data, dtype = np.short)
    wave_data.shape = -1, 256
    wave_data = wave_data.T

    #print wave_data.shape
    means = np.mean(wave_data, axis=0)
    valids = (np.abs(means) > 3) * means

    #plt.plot(range(0, means.shape[0]), means)
    #plt.show()

    tmpMin = 0
    tmpMax = 0
    flag = False
    pairs = []
    for i in range(0, len(valids)):
        if flag == False:
            if valids[i] != 0:
                tmpMin = i
                tmpMax = i
                flag = True
        else:
            if valids[i] == 0:
                tmpMax = i - 1
                pairs.append((tmpMin, tmpMax))
                flag = False
    if flag == True:
        pairs.append((tmpMin, len(valids) - 1))

    valid_pairs = []
    flag = False
    for i in range(0, len(pairs) - 1):
        if flag == False:
            if pairs[i + 1][0] - pairs[i][1] <= 20:
                tmpMin = pairs[i][0]
                tmpMax = pairs[i + 1][1]
                flag = True
        else:
            if pairs[i + 1][0] - pairs[i][1] <= 20:
                tmpMax = pairs[i + 1][1]
            else:
                valid_pairs.append((tmpMin, tmpMax))
                flag = False
    if flag == True:
        valid_pairs.append((tmpMin, pairs[-1][1]))

    valid_datas = []
    for i in range(0, len(valid_pairs)):
        valid_datas.append(wave_data[:, valid_pairs[i][0]:valid_pairs[i][1]])

    return valid_datas