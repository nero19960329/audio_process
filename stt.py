import configs
import os.path
import json
import pycurl
import uuid
import wave
import urllib2
import seperate_wav as sw
import extract_feature as ef
import sys
from sklearn.externals import joblib
from StringIO import StringIO
import numpy as np

def predict(wav_data, modelName='./classifier.model'):
    #data = sw.seperate(fileName)
    mfcc = ef.extract_feature_single(wav_data)
    classifier = joblib.load(modelName)
    probabilities = np.mean(classifier.predict(mfcc), axis=0)
    return np.argmax(probabilities)

def get_mac_address():
    return uuid.UUID(int=uuid.getnode()).hex[-12:]

def get_token():
    url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + configs.API_KEY + "&client_secret=" + configs.SECRET_KEY
    res = urllib2.urlopen(url).read()
    data = json.loads(res)
    token = data['access_token']
    return token

def dump_res(buf):
    resp_json = json.loads(buf.decode('utf-8'))
    global ret_text
    if resp_json['err_no'] == 3301:
        ret_text = "Recognition error."
    else:
        ret = resp_json['result']
        ret_text = ret[0]

def get_json(token, wav_data):
    size = len(wav_data)

    url = "http://vop.baidu.com/server_api?cuid=" + get_mac_address() + "&token=" + token
    http_header = [
        "Content-Type: audio/pcm; rate=16000"
        "Content-Length: %d" % size
    ]

    c = pycurl.Curl()
    c.setopt(pycurl.URL, str(url)) 
    c.setopt(c.HTTPHEADER, http_header) 
    c.setopt(c.POST, 1) 
    c.setopt(c.CONNECTTIMEOUT, 30) 
    c.setopt(c.TIMEOUT, 30)
    c.setopt(c.WRITEFUNCTION, dump_res)
    c.setopt(c.POSTFIELDS, wav_data)
    c.setopt(c.POSTFIELDSIZE, size)
    c.perform() 

    return ret_text

def get_words(token, fileName):
    return get_json(token, fileName)

if __name__ == '__main__':
    token = get_token()
    wave_data_list = []
    authors = None
    if len(sys.argv) < 2:
        print 'Error arguments'
        exit()
    elif len(sys.argv) == 2:
        wave_data_list = sw.seperate(sys.argv[1])
        authors = joblib.load('./authors.pickle')
    else:
        wave_data_list = sw.seperate(sys.argv[1])
        authors = joblib.load(sys.argv[2])
        
    for data in wave_data_list:
        wave_data = data.T.tostring()
        if len(wave_data) < 10000:
            continue
        print '%s: %s' % (authors[predict(data)], get_words(token, wave_data))