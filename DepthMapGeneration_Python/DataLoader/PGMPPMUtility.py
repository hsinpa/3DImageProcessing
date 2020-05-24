from DataLoader.LoaderUtility import LoaderUtility
from typing import List
import os, os.path

class PGMPPMUtility:

    def __init__(self, allFoldersDict:dict, outputPath:str):
        self.loader = LoaderUtility()
        self.allFoldersDict = allFoldersDict
        self.outputPath = outputPath

    def PairDepthImageToSelectFile(self, colorImgPath:str, depthImgPath:str, imageType:str):
        for folderpath, filePathList in self.allFoldersDict.items():

            for filepath in filePathList:
                colorFullPath = folderpath + filepath+'/'+colorImgPath
                depthFullPath = folderpath + filepath+'/'+depthImgPath

                isColorExist = os.path.exists(colorFullPath)
                isDepthExist = os.path.exists(depthFullPath)

                if (isColorExist and isDepthExist):
                    colorNewFileName = self.loader.ChangeImageFileType(colorFullPath, imageType)
                    depthNewFileName = self.loader.ChangeImageFileType(depthFullPath, imageType)

                    self.loader.resize_canvas(colorFullPath, self.outputPath +"/Raw/" + colorNewFileName, img_type=imageType, canvas_width=128, canvas_height=128)
                    self.loader.resize_canvas(depthFullPath, self.outputPath +"/Depth/" + depthNewFileName, img_type=imageType, canvas_width=128, canvas_height=128)
                    return

                # loader.GetFileType(filepath)
                # colorPath = GetImageFromPath(folderpath + filepath + '/', ['.ppm'])
                # depthPath = GetImageFromPath(folderpath + filepath + '/', ['.pgm'])

    def ProcessIndexFile(self, indexPath: str):
        file1 = open(indexPath, 'r')
        Lines = file1.readlines()

        count = 0
        cachePGMFile = ''

        for line in Lines:
            # print(line.strip())
            filepath = line.strip()
            fileType = self.loader.GetFileType(filepath)
            if (fileType == 'dump'):
                continue

            if (fileType == 'pgm'):
                cachePGMFile = filepath
                continue

            # Do actual stuff here
            if (fileType == 'ppm'):
                self.PairDepthImageToSelectFile(colorImgPath=filepath, depthImgPath=cachePGMFile, imageType='jpeg')
                cachePGMFile = ''
            # print("Line{}: {}".format(count, line.strip()))

        file1.close()