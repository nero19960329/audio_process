import seperate_wav as sw
import extract_feature as ef
import numpy as np
import os
import os.path
import stt
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.externals import joblib

wav_path = r'./wav/'

def train(data, label):
    train_data = data
    train_label = label
    print "Training . . ."
    rf = RandomForestRegressor()
    rf.fit(train_data, train_label)
    print "Done!"

    return rf

def batch_train():
    author_cnt = 0
    author_map = {}
    dirnames = [f for f in os.listdir(wav_path) if os.path.isdir(os.path.join(wav_path, f))]
    author_cnt = len(dirnames)
    author_list = []
    cnt = 0
    for dirname in dirnames:
        author_map[dirname] = cnt
        author_list.append(dirname)
        cnt += 1

    train_data = np.ndarray((0, 13), dtype=np.float32)
    train_label = np.ndarray((0, author_cnt), dtype=np.float32)
    test_data = []

    for _, dirnames, _ in os.walk(wav_path):
        for dirname in dirnames:
            for _, _, filenames in os.walk(os.path.join(wav_path, dirname)):
                cnt = 0
                for filename in filenames:
                    data = sw.seperate(os.path.join(wav_path, dirname, filename))
                    mfcc = ef.union_feature(ef.extract_feature(data))
                    label = np.zeros((mfcc.shape[0], author_cnt), dtype=np.float32)
                    label[:, author_map[dirname]] = np.ones((mfcc.shape[0]), dtype=np.float32)
                    if cnt < 9:
                        train_data = np.row_stack((train_data, mfcc))
                        train_label = np.row_stack((train_label, label))
                    else:
                        test_data.append(mfcc)

                    cnt += 1

    classifier = train(train_data, train_label)
    joblib.dump(classifier, 'classifier.model')
    joblib.dump(author_list, 'authors.pickle')

    for i in range(0, len(test_data)):
        print np.mean(classifier.predict(test_data[i]), axis=0)

    return classifier


def main():
    classifier = batch_train()
    joblib.dump(classifier, 'classifier.model')

if __name__ == "__main__":
    main()