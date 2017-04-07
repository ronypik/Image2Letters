"""
returns rectangles containing possible licence plates from a given image
for parameters see
http://docs.opencv.org/3.0-beta/modules/objdetect/doc/cascade_classification.html

python3 rekkariDetectionSave.py 0-751.jpg
(there must be trained classifiier file, assumption is 'rekkari.xml' )
"""

import numpy as np
import cv2
from matplotlib import pyplot as plt
from glob import glob
import sys
import os

class DetectPlate():

    def __init__(self, trainedHaarFileName='/home/mka/PycharmProjects/Image2Letters/rekkari.xml',
                imageFileName=None,
                detectFactor=5, scaleFactor=1.03, minSize=(5,18),
                colorConversion=cv2.COLOR_BGR2GRAY):

        if not os.path.isfile(trainedHaarFileName):
            raise FileNotFoundError('you need cascade training file for cv2.CascadeClassifier')
        self.trainedHaarFileName = trainedHaarFileName
        self.cascade = cv2.CascadeClassifier(trainedHaarFileName)
        self.imageFileName = imageFileName
        self.detectFactor = detectFactor
        self.scaleFactor = scaleFactor
        self.minSize = minSize
        self.colorConversion = colorConversion
        self.img = None
        self.gray = None
        self.plates = None
        self.npPlates = []  #images of plate(s) as array of numpy arrays

    def image2Plates(self):
        """ from image, produce rectangle(s) that contain possible plate, output as list of rectanges"""
        if not os.path.isfile(self.imageFileName):
            raise FileNotFoundError('NO imagefile with name: ' + self.imageFileName)
        self.img = cv2.imread(self.imageFileName)
        self.gray = cv2.cvtColor(self.img.copy(), self.colorConversion)
        rectangles = self.cascade.detectMultiScale(self.gray, self.scaleFactor, self.detectFactor, minSize=self.minSize)
        plates = []
        for [x,y,w,h] in rectangles:
            plates.append([x,y,w,h])
        self.plates = plates

    def image2PlateNumpyArrays(self):
        """ from image, produce rectangle(s) that contain possible plate,
        output as list of numpy array(s) representing gray scale images(s) about possible plates"""
        if not os.path.isfile(self.imageFileName):
            raise FileNotFoundError('NO imagefile with name: ' + self.imageFileName)
        self.npPlates = []
        self.img = cv2.imread(self.imageFileName)
        self.gray = cv2.cvtColor(self.img.copy(), self.colorConversion)
        rectangles = self.cascade.detectMultiScale(self.gray, self.scaleFactor, self.detectFactor, minSize=self.minSize)
        for [x,y,w,h] in rectangles:
            roi_gray = self.gray[y:y+h, x:x+w]
            self.npPlates.append(roi_gray)

    def getNpPlates(self):
        """ give found plate(s) as array of numpy arrays"""
        self.image2PlateNumpyArrays()
        return self.npPlates


    def getGray(self):
        return self.gray.copy()


    def showPlates(self):
        self.image2Plates()
        clone = self.getGray().copy()
        for i, [x,y,w,h] in enumerate(self.plates):
            print("xywh",x,y,w,h)
            cv2.rectangle(clone,(x,y),(x+w,y+h),(0,255,0),5)
        cv2.imshow('clone', clone)
        while(cv2.waitKey()!=ord('q')):
            continue


    def writePlates(self):
        self.image2Plates()
        clone = self.getGray().copy()
        for i, [x,y,w,h] in enumerate(self.plates):
            print("xywh",x,y,w,h)
            roi_gray = clone[y:y+h, x:x+w]
            cv2.imwrite(str(i)+'-'+'plate'+'-'+sys.argv[1]+'.tif', roi_gray)

if __name__ == '__main__':
    import sys
    app = DetectPlate(imageFileName=sys.argv[1], detectFactor=1)
    app.writePlates()
    #app.showPlates()




