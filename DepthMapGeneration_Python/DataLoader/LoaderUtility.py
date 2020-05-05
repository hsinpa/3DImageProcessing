import os, os.path

import cv2
import numpy as np
from PIL import Image
import math
from typing import List

class LoaderUtility:

    def GetAllFolderNameFromPath(self, path : str) -> List[str]:
        return [item for item in os.listdir(path) if os.path.isdir(os.path.join(path, item))]

    def GetRawImageFromPath(self, p_path: str, p_valid_formats: List[str]):
        path = []

        for f in os.listdir(p_path):
            ext = os.path.splitext(f)[1]
            if ext.lower() not in p_valid_formats:
                continue

            path.append(p_path + f)

        return path

    def GetCVImageFromPath(self, p_path: str, colorType : int):
        sets = []

        for f in os.listdir(p_path):
            image = cv2.imread(p_path+f,  colorType)
                               #cv2.COLOR_BGR2RGB)
            #print(image)
            sets.append(image)

        return sets

    def GetLabelIndexFromImages(self, image_name: str, labels):
        label_s_index = image_name.rfind("_") + 1

        label = image_name[label_s_index:-4]
        return labels.index(label)

    def GetDatasetFromPath(self, p_path: str, p_valid_formats: List[str], p_define_label: List[str], p_normalizedFunc):
        imgs = []
        labels = []

        for f in os.listdir(p_path):
            ext = os.path.splitext(f)[1]
            if ext.lower() not in p_valid_formats:
                continue

            #Append Labels only if its exist
            if (p_define_label == None and len(p_define_label) > 0):
                labels.append(self.GetLabelIndexFromImages(f, p_define_label))

            image = cv2.imread(p_path+f,  cv2.COLOR_BGR2RGB)
            if p_normalizedFunc != None:
                image = p_normalizedFunc(image)

            imgs.append(image)
        return np.asarray(imgs), np.asarray(labels)

    def ChangeImageFileType(self, path, fileType):
        lastIndex = path.rindex("/") + 1
        return path[lastIndex:-3] + fileType

    def shuffle(self, x, y):
        idx = np.random.permutation(len(x))
        return x[idx], y[idx]

    def RewriteImagePath(self, path, label, image):
        fileCount = len( os.listdir(path))
        fileName = "{}/gesture_{}_{}.png".format(path, fileCount, label)
        cv2.imwrite(fileName, image)

    def FlipImage(self, raw_image):
        newImgs = []

        newImgs.append(cv2.flip(raw_image, 1))
        newImgs.append(cv2.flip(raw_image, 0))
        newImgs.append(cv2.flip(raw_image, -1))
        return newImgs

    def Normalized(self, image):
        return image / 255

    def TanhNormalized(self, image):
        return (image - 127.5) / 127.5

    def resize_canvas(self, old_image_path : str ="314.jpg", new_image_path : str ="save.jpg", img_type : str = "JPEG",
                      canvas_width : int =500, canvas_height : int =500):
        """
        Resize the canvas of old_image_path.

        Store the new image in new_image_path. Center the image on the new canvas.

        Parameters
        ----------
        old_image_path : str
        new_image_path : str
        canvas_width : int
        canvas_height : int
        """
        im = Image.open(old_image_path).convert("RGB")
        old_width, old_height = im.size

        mode = im.mode
        new_background = (255, 255, 255)
        if len(mode) == 1:  # L, 1
            new_background = (255)
        if len(mode) == 3:  # RGB
            new_background = (255, 255, 255)
        if len(mode) == 4:  # RGBA, CMYK
            new_background = (255, 255, 255, 255)

        if (old_height > canvas_height or old_width > canvas_width or ( abs(old_height - old_width) < 50)):
            wpercent = (canvas_width / old_width)
            hsize = int((float(old_height) * float(wpercent)))
            im = im.resize((canvas_width, hsize), Image.ANTIALIAS)

            hpercent = (canvas_height / old_height)
            wsize = int((float(old_width) * float(hpercent)))
            im = im.resize((wsize, canvas_height), Image.ANTIALIAS)

        old_width, old_height = im.size

        # Center the image
        x1 = int(math.floor((canvas_width - old_width) / 2))
        y1 = int(math.floor((canvas_height - old_height) / 2))

        newImage = Image.new("RGB", (canvas_width, canvas_height), new_background)
        newImage.paste(im, (x1, y1, x1 + old_width, y1 + old_height))

        newImage.save(new_image_path, img_type)