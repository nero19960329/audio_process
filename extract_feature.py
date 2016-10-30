from python_speech_features import mfcc
import numpy as np
import configs

def extract_feature(datas):
    features = []
    for i in range(len(datas)):
        tmp_list = []
        for j in range(datas[i].shape[1]):
            tmp_list.append(mfcc(datas[i][:, j], configs.framerate))
        features.append(union_feature(tmp_list))

    return features

def extract_feature_single(data):
    feature = np.ndarray((data.shape[1], 13), dtype=np.float32)
    for i in range(data.shape[1]):
        feature[i, :] = mfcc(data[:, i], configs.framerate)
    return feature

def union_feature(features):
    matrix = np.ndarray((0, 13), dtype=np.float32)
    for feature in features:
        matrix = np.row_stack((matrix, feature))
    return matrix