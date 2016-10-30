import numpy as np
from pyaudio import PyAudio, paInt16
import wave
import sys, os
import configs
import msvcrt

def save_wave_file(fileName, data):
    wf = wave.open(fileName, 'wb')
    wf.setnchannels(configs.channels)
    wf.setsampwidth(configs.sampwidth)
    wf.setframerate(configs.framerate)
    wf.writeframes("".join(data))
    wf.close()

def record_wave(name, time):
    pa = PyAudio()
    stream = pa.open(format = paInt16, channels = 1, rate = configs.framerate, input = True, frames_per_buffer = configs.NUM_SAMPLES)
    save_buffer = []
    count = 0
    print "Press Enter to start recording . . ."
    msvcrt.getch()
    print "File " + name + ".wav recording . . ."
    for i in range(0, int(configs.framerate / configs.NUM_SAMPLES * time)):
        string_audio_data = stream.read(configs.NUM_SAMPLES)
        save_buffer.append(string_audio_data)
        count += 1

    fileName = name + ".wav"
    save_wave_file(fileName, save_buffer)
    save_buffer = []
    print fileName, "saved"

def main():
    if len(sys.argv) < 4:
        print "Error arguments!"
        exit()
    elif len(sys.argv) == 4:
        if sys.argv[1] == "-train":
            author = sys.argv[2]
            count = int(sys.argv[3])
            folder_path = r'./wav/' + author + r'/'
            if not os.path.isdir(folder_path):
                os.mkdir(folder_path)
            for i in range(0, count):
                record_wave(os.path.join(folder_path, '%d' % i), configs.TIME)
        elif sys.argv[1] == "-dialogue":
            folder_path = r'./wav/'
            fileName = sys.argv[2]
            time = int(sys.argv[3])
            record_wave(os.path.join(folder_path, fileName), time)

if __name__ == "__main__":
    main()