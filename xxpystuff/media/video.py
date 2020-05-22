#!/usr/bin/env python3 

import os, sys, cv2


class Video:

   def __init__(self, fileName):

      if not fileName.endswith('.mp4'):
         raise ValueError

      codec = cv2.VideoWriter_fourcc(*'mp4v')
      fps = 30
      self._targetSize = (1920, 1080)
      self._video = cv2.VideoWriter(fileName, codec, fps, self._targetSize)      


   def __del__(self):

      self._video.release()

   def addImage(self, imagePath):

      imageData = cv2.imread(imagePath)
      image = cv2.resize(imageData, self._targetSize, interpolation = cv2.INTER_LANCZOS4)
      self._video.write(image)

   @staticmethod
   def fromDirectory(imageDirectory, videoName, statusindicator = None):

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

      count = len(imageList)
      for index in range(count):
         if statusindicator:
            statusindicator.progress(index, count)
         imagePath = imageList[index]
         video.writeImage(imagePath)

      if statusindicator:
         statusindicator.endProgress()

   @staticmethod
   def toDirectory(imageDirectory, videoName, statusindicator = None):

      if not os.path.exists(videoName):
         return

      os.makedirs(imageDirectory)

      if statusindicator:
         statusindicator.setProgressText('creating image sequence')

      video = cv2.VideoCapture(videoName)
      width = video.get('CV_CAP_PROP_FRAME_WIDTH')
      height = video.get('CV_CAP_PROP_FRAME_HEIGHT')

      """
      while(video.isOpened()):
         ret, frame = video.read()
      """
      if statusindicator:
         statusindicator.endProgress()

      print(width, height)

class VideoBlend(Video):

   def __init__(self, fileName, framesPerImage = 30):

      Video.__init__(self, fileName)

      self._framesPerImage = framesPerImage
      self._lastImage = None


   def __del__(self):

      if self._lastImage is not None:
         self._video.write(self._lastImage)
      Video.__del__(self)

   def addImage(self, imageData):

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
   def fromDirectory(imageDirectory, videoName, statusindicator = None):

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
         image = cv2.resize(imageData, video._targetSize, interpolation = cv2.INTER_LANCZOS4)
         video._video.write(image)

      if statusindicator:
         statusindicator.endProgress()
