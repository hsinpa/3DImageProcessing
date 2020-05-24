from DataLoader.LoaderUtility import LoaderUtility
from DataLoader.PGMPPMUtility import PGMPPMUtility
from typing import List
import os, os.path

folders = [""]
path1 = "../Dataset/TouhouDataset/Other/"
path2 = "../Dataset/TouhouDataset/Marisa/"
path3 = "../Dataset/TouhouDataset/Reimu/"

valid_images = [".jpg",".png", ".pgm", ".ppm"]
labels = []


def GetImageFromPath(p_path: str, p_valid_formats: List[str]):
    path = []

    for f in os.listdir(p_path):
        ext = os.path.splitext(f)[1]
        if ext.lower() not in p_valid_formats:
            continue

        path.append(p_path + f)

    return path

resizeFolder = "../Dataset/ResizePGM"
indoorTestPath = '../Dataset/PGMPPM/cafe/'
indoorTrainPath = '../Dataset/indoor_train/train/LR/'
indexFilePath = '../Dataset/PGMPPM/cafe/cafe_0001c/INDEX.txt'

loader = LoaderUtility()

indoorTestFolders = loader.GetAllFolderNameFromPath(indoorTestPath)
# indoorTrainFolders = loader.GetAllFolderNameFromPath(indoorTrainPath)

allFolders = {indoorTestPath: indoorTestFolders}
pgmUtility = PGMPPMUtility(allFolders, resizeFolder)

pgmUtility.ProcessIndexFile(indexFilePath)
