
from DataLoader.LoaderUtility import LoaderUtility
from typing import List
import os, os.path

valid_images = [".jpg",".png", ".tif", '.tiff', '.jpeg']
labels = []



def GetImageFromPath(p_path: str, p_valid_formats: List[str]):
    path = []

    for f in os.listdir(p_path):
        ext = os.path.splitext(f)[1]
        if ext.lower() not in p_valid_formats:
            continue

        path.append(p_path + f)

    return path

# resizeFolder = "../Dataset/ResizeImage/Train"
resizeFolder = "../Dataset/WantData"

indoorTestPath = '../Dataset/indoor_test/test/LR/'
indoorTrainPath = '../Dataset/indoor_train/train/LR/'

directPath = '../Dataset/WantData'

loader = LoaderUtility()

indoorTestFolders = loader.GetAllFolderNameFromPath(indoorTestPath)
indoorTrainFolders = loader.GetAllFolderNameFromPath(indoorTrainPath)

allFolders = {indoorTestPath: indoorTestFolders, indoorTrainPath: indoorTrainFolders}

# for folderpath, filePathList in allFolders.items():
#
#     for filepath in filePathList:
#         colorPath = GetImageFromPath(folderpath + filepath + "/color/", valid_images)
#         depthPath = GetImageFromPath(folderpath + filepath + "/depth_vi/", valid_images)
#
#         for i in range(len(colorPath)):
#             colorNewFileName = loader.ChangeImageFileType(colorPath[i], "jpeg")
#             depthNewFileName = loader.ChangeImageFileType(depthPath[i], "jpeg")
#             loader.resize_canvas(colorPath[i], resizeFolder +"/Raw/" + colorNewFileName, img_type="jpeg", canvas_width=128, canvas_height=128)
#             loader.resize_canvas(depthPath[i], resizeFolder +"/Depth/" + depthNewFileName, img_type="jpeg", canvas_width=128, canvas_height=128)

#
colorPath = GetImageFromPath(directPath + "/scene3_color/", valid_images)
depthPath = GetImageFromPath(directPath + "/scene3_depth/", valid_images)

for i in range(len(colorPath)):
    fileType = 'jpeg'

    imageName = 'human_scene3_' + str(i) + '_'
    colorName = loader.GetImageName(imageName + 'c', fileType)
    depthName = loader.GetImageName(imageName + 'depth_vi', fileType)

    loader.resize_canvas(colorPath[i], resizeFolder +"/Raw/" + colorName, img_type=fileType, canvas_width=128, canvas_height=128)
    loader.resize_canvas(depthPath[i], resizeFolder +"/Depth/" + depthName, img_type=fileType, canvas_width=128, canvas_height=128)

#
# depthPath = GetImageFromPath(directPath + "/Test/", valid_images)
# for i in range(len(depthPath)):
#     fileType = 'jpeg'
#
#     depthNewFileName = directPath + "/Test/"+loader.ChangeImageFileType(depthPath[i], fileType)
#     print(depthNewFileName)
#
#     loader.ConvertImageType(image_path=depthPath[i], file_name=depthNewFileName)
