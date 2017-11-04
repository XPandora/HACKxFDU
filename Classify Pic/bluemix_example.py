import json
from os.path import join, dirname
from os import environ
from watson_developer_cloud import VisualRecognitionV3
import os
import time
visual_recognition = VisualRecognitionV3('2016-05-20', api_key='688c40044862a98b6e291f0cf0c9fb24eaf84ab3')


def Classify_image():
    rootdir = 'C:\\Users\\clive\\Desktop\\test'
    list = os.listdir(rootdir)
    for i in range(0,len(list)):
        path = os.path.join(rootdir,list[i])
        if os.path.isfile(path):
            f = open(path,'rb')
            print(path)
            print(json.dumps(visual_recognition.classify(images_file=f), indent=2))
            print('\n')
    return

def main():
    Classify_image()
    return




def Classify(rootdir):
    list = os.listdir(rootdir)
    for i in range(0,len(list)):
        path = os.path.join(rootdir,list[i])
        if os.path.isfile(path):
            f = open(path,'r')
            filename[i] = path # list of each file direction
            returns[i] = json.dumps(visual_recognition.classify(images_file=f), indent=2) #list of classify result
    return filename,returns

def test():
    f = open('C://Python27//Wall Paper.zip','rb')
    print(json.dumps(visual_recognition.classify(images_file=f), indent=2))
            
main()
