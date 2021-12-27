#!/usr/bin/env python3

import os
import cv2


class Video:

    FullHD = (1920, 1080)
    UltraHD = (3840, 2160)

    def __init__(self, fileName, targetSize, fps=30):

        if not fileName.endswith('.mp4'):
            raise ValueError

        codec = cv2.VideoWriter_fourcc(*'mp4v')
        self._targetSize = targetSize
        self._video = cv2.VideoWriter(fileName, codec, fps, self._targetSize)

    def __del__(self):

        self._video.release()

    def addImage(self, image):

        self._video.write(image)

    def addImageFile(self, imagePath):

        imageData = cv2.imread(imagePath)
        image = cv2.resize(imageData, self._targetSize, interpolation=cv2.INTER_LANCZOS4)
        self._video.write(image)

    @staticmethod
    def fromDirectory(imageDirectory, videoName, statusindicator=None):

        imageList = list()

        for entry in os.scandir(imageDirectory):
            if entry.name.endswith('.png'):
                imageList.append(entry.path)

        imageList.sort()
        if not imageList:
            return

        if statusindicator:
            statusindicator.setProgressText('creating video')

        video = Video(videoName)

        total = len(imageList)
        for index in range(total):
            if statusindicator:
                statusindicator.progress(index, total)
            imagePath = imageList[index]
            video.addImageFile(imagePath)

        if statusindicator:
            statusindicator.endProgress()

    @staticmethod
    def toDirectory(imageDirectory, videoName, statusindicator=None):

        if not os.path.exists(videoName):
            return

        imageDirectory = os.path.abspath(imageDirectory)
        if not imageDirectory.endswith('/'):
            imageDirectory = imageDirectory + '/'
        os.makedirs(imageDirectory, exist_ok=True)

        if statusindicator:
            statusindicator.setProgressText('creating image sequence')

        video = cv2.VideoCapture(videoName)

        total = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

        def calcPadding():
            test = 10
            padding = 1
            while test < total:
                test *= 10
                padding += 1
            return padding

        padding = calcPadding()
        index = 1

        while(video.isOpened()):
            grabbed, frame = video.read()
            if not grabbed:
                break
            if statusindicator:
                statusindicator.progress(index, total)
            num = str(index)
            index += 1
            while len(num) < padding:
                num = '0' + num
            name = imageDirectory + 'image_' + num + '.png'
            try:
                cv2.imwrite(name, frame)
            except:
                pass

        if statusindicator:
            statusindicator.endProgress()


class VideoBlend(Video):

    def __init__(self, fileName, framesPerImage=30):

        Video.__init__(self, fileName)

        self._framesPerImage = framesPerImage
        self._lastImage = None

    def __del__(self):

        if self._lastImage is not None:
            self._video.write(self._lastImage)
        Video.__del__(self)

    def addImageFile(self, imageData):

        if self._lastImage is None:
            self.writeImage(imageData)
        else:
            for frame in range(self._framesPerImage):
                alpha = frame * (1.0 / self._framesPerImage)
                beta = 1.0 - alpha
                mixed = cv2.addWeighted(self._lastImage, beta, imageData, alpha, 0.0)
                self.writeImage(mixed)

        self._lastImage = imageData

    @staticmethod
    def fromDirectory(imageDirectory, videoName, statusindicator=None):

        imageList = list()

        for entry in os.scandir(imageDirectory):
            if entry.name.endswith('.png'):
                imageList.append(entry.path)

        imageList.sort()
        if not imageList:
            return

        if statusindicator:
            statusindicator.setProgressText('creating video')

        video = VideoBlend(videoName)

        count = len(imageList)
        for index in range(count):
            if statusindicator:
                statusindicator.progress(index, count)
            imagePath = imageList[index]
            imageData = cv2.imread(imagePath)
            image = cv2.resize(imageData, video._targetSize, interpolation=cv2.INTER_LANCZOS4)
            video._video.write(image)

        if statusindicator:
            statusindicator.endProgress()
