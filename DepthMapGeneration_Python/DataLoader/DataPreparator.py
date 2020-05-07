from DataLoader.LoaderUtility import LoaderUtility
import numpy as np

class DataPreparator():

    def __init__(self, x_path:str, x_imageType:int, y_path:str, y_imageType:int):
        self.dataLoader = LoaderUtility()

        self.x_path = x_path
        self.y_path = y_path
        self.x_imageType = x_imageType
        self.y_imageType = y_imageType

    def GetTrainTestSet(self, ratio:float, useAugmentation : bool = False):
        xSet, ySet = self.GetXYDataSet()
        trainLength = int(len(xSet) * ratio)

        if (useAugmentation):
            xSet.extend( self.dataLoader.FlipImages(xSet))
            ySet.extend( self.dataLoader.FlipImages(ySet))

        # return np.array(xSet[:-trainLength]) / 255.0, np.array(ySet[:-trainLength]) / 255.0, \
        #        np.array(xSet[-trainLength:]) / 255.0, np.array(ySet[-trainLength:]) / 255.0
        return np.array(self.dataLoader.TanhData(xSet[:-trainLength], 255.0)), np.array(self.dataLoader.TanhData(ySet[:-trainLength], 255.0)),\
               np.array(self.dataLoader.TanhData(xSet[-trainLength:], 255.0)), np.array(self.dataLoader.TanhData(xSet[-trainLength:], 255.0))

    def GetXYDataSet(self):

        colorset = self.dataLoader.GetCVImageFromPath(self.x_path, self.x_imageType)
        depthset = self.dataLoader.GetCVImageFromPath(self.y_path, self.y_imageType)

        return colorset, depthset

