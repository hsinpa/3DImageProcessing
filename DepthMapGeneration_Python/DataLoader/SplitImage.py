
from DataLoader.LoaderUtility import LoaderUtility
from typing import List
import os, os.path
import cv2
import numpy as np
from PIL import Image
import math
import PIL.ImageOps as ImageOps


valid_images = [".jpg",".png", ".tif", '.tiff', '.jpeg']
labels = []
loader = LoaderUtility()

def ChangeColorDepthToGray(p_path):
    im = Image.open(p_path).convert("RGB")
    pixelMap = im.load()

    img = Image.new(im.mode, im.size)
    pixelsNew = img.load()
    for x in range(img.size[0]):
        for y in range(img.size[1]):

            Red = pixelMap[x, y][0]
            Green = pixelMap[x, y][1]
            Blue = pixelMap[x, y][2]

            nRed = pixelMap[x, y][0] / 255.0
            nGreen = pixelMap[x, y][1] / 255.0
            nBlue = pixelMap[x, y][2] / 255.0

            GE = (nGreen * 0.5)

            scale = 0.9
            Gray = ((-1 * nBlue) + (1 * nRed)) * (1 - GE)
            Gray = (Gray + 1) * 0.5 * scale

            if ((Red < 3 and Green < 3 and Blue > 127 ) or (Blue < 3 and Green < 3 and Red > 127)):
                max = 255.0

                if (nRed > nBlue):
                    residual = (1 - (Red / max)) * 0.1
                    Gray = scale + residual
                else:
                    residual = (1 - (Blue / max)) * 0.1
                    Gray = (1-scale) - residual

            Gray = 255 - int(Gray * 255)
            pixelsNew[x, y] = (Gray, Gray, Gray)

    im.close()
    img.show()
    img.save(p_path)
    img.close()

def GetImageFromPath(p_path: str, p_valid_formats: List[str]):
    path = []

    for f in os.listdir(p_path):
        ext = os.path.splitext(f)[1]
        if ext.lower() not in p_valid_formats:
            continue

        path.append(p_path + f)

    return path

# resizeFolder = "../Dataset/ResizeImage/Train"
resizeFolder = "../Dataset/BlenderTest"

rawPath = '../Dataset/StreetShot/raw/'
colorPath = '../Dataset/StreetShot/color/'
depthPath = '../Dataset/StreetShot/depth/'

rawPath = GetImageFromPath(rawPath, valid_images)
allDepthImage = GetImageFromPath(depthPath, valid_images)

# colorPath = GetImageFromPath(directPath + "/color/", valid_images)
# depthPath = GetImageFromPath(directPath + "/depth_vi/", valid_images)

fileType = 'jpeg'
boxSize = (256, 256)
outputSize = (128, 128)

c_x = 0
c_y = 0
c_width = 256
c_height = 256
colorArea = (c_x, c_y, c_width, c_height)

d_x = 256
d_y = 0
d_width = 512
d_height = 256
depthArea = (d_x, d_y, d_width, d_height)

for i in range(len(allDepthImage)):
    ChangeColorDepthToGray(allDepthImage[i])



# for i in range(len(rawPath)):
#
#     imageName = 'street_' + str(i) + '_'
#     colorFullPath = colorPath + loader.GetImageName(imageName + 'c', fileType)
#     depthFullPath = depthPath + loader.GetImageName(imageName + 'depth_vi', fileType)
#
#     loader.SplitDepthPairImage(image_path=rawPath[i], color_area=colorArea, depth_area=depthArea,
#                                 output_color_path=colorFullPath, output_depth_path=depthFullPath, output_size=outputSize, img_type=fileType)
#     # colorNewFileName = loader.ChangeImageFileType(colorPath[i], fileType)
#     # depthNewFileName = loader.ChangeImageFileType(depthPath[i], fileType)
#     #
#     # imageName = 'human_' + str(i) + '_'
#     # colorName = loader.GetImageName(imageName + 'c', fileType)
#     # depthName = loader.GetImageName(imageName + 'depth_vi', fileType)
#     #
#     # loader.resize_canvas(colorPath[i], resizeFolder +"/Raw/" + colorName, img_type=fileType, canvas_width=128, canvas_height=128)
#     # loader.resize_canvas(depthPath[i], resizeFolder +"/Depth/" + depthName, img_type=fileType, canvas_width=128, canvas_height=128)
