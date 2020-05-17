
from DataLoader.LoaderUtility import LoaderUtility
from typing import List
import os, os.path

folders = [""]
path1 = "../Dataset/TouhouDataset/Other/"
path2 = "../Dataset/TouhouDataset/Marisa/"
path3 = "../Dataset/TouhouDataset/Reimu/"
resizeFolder = "../Dataset/TouhouDataset/ResizeFolder/"

valid_images = [".jpg",".png"]
labels = []


def GetImageFromPath(p_path: str, p_valid_formats: List[str]):
    path = []

    for f in os.listdir(p_path):
        ext = os.path.splitext(f)[1]
        if ext.lower() not in p_valid_formats:
            continue

        path.append(p_path + f)

    return path

resizeFolder = "../Dataset/ResizeImage/Train"
indoorTestPath = '../Dataset/indoor_test/test/LR/'
indoorTrainPath = '../Dataset/indoor_train/train/LR/'

loader = LoaderUtility()

indoorTestFolders = loader.GetAllFolderNameFromPath(indoorTestPath)
indoorTrainFolders = loader.GetAllFolderNameFromPath(indoorTrainPath)

allFolders = {indoorTestPath: indoorTestFolders, indoorTrainPath: indoorTrainFolders}

for folderpath, filePathList in allFolders.items():

    for filepath in filePathList:
        colorPath = GetImageFromPath(folderpath + filepath + "/color/", valid_images)
        depthPath = GetImageFromPath(folderpath + filepath + "/depth_vi/", valid_images)

        for i in range(len(colorPath)):
            colorNewFileName = loader.ChangeImageFileType(colorPath[i], "jpeg")
            depthNewFileName = loader.ChangeImageFileType(depthPath[i], "jpeg")
            loader.resize_canvas(colorPath[i], resizeFolder +"/Raw/" + colorNewFileName, img_type="jpeg", canvas_width=128, canvas_height=128)
            loader.resize_canvas(depthPath[i], resizeFolder +"/Depth/" + depthNewFileName, img_type="jpeg", canvas_width=128, canvas_height=128)