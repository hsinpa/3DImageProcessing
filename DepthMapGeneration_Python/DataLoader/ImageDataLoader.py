import numpy as np
import cv2
from tensorflow.keras.utils import Sequence
import random

class ImageDataLoader(Sequence):
    """Generates data for Keras
    Sequence based data generator. Suitable for building data generator for training and prediction.
    """
    def __init__(self, list_IDs, image_path, label_path,
                 to_fit=True, batch_size=32, dim=(256, 256),
                 input_channels=1, output_channels=1, input_image_type=0, output_image_type=0, shuffle=True, augmentation=None, initSeed=1):
        """Initialization
        :param list_IDs: list of all 'label' ids to use in the generator
        :param image_path: path to images location
        :param label_path: path to masks location
        :param to_fit: True to return X and y, False to return X only
        :param batch_size: batch size at each iteration
        :param dim: tuple indicating image dimension
        :param input_channels: number of image channels
        :param output_channels: number of output masks
        :param input_image_type: OpenCV Image Type
        :param output_image_type: OpenCV Image Type
        :param shuffle: True to shuffle label indexes after every epoch
        """
        self.list_IDs = list_IDs
        self.image_path = image_path
        self.label_path = label_path
        self.to_fit = to_fit
        self.batch_size = batch_size
        self.dim = dim
        self.input_channels = input_channels
        self.output_channels = output_channels
        self.input_image_type = input_image_type
        self.output_image_type = output_image_type
        self.shuffle = shuffle
        self.augmentation = augmentation
        self.seed = initSeed
        self.epochNum = 0
        self.on_epoch_end()

    def __len__(self):
        """Denotes the number of batches per epoch
        :return: number of batches per epoch
        """
        return int(np.floor(len(self.list_IDs) / self.batch_size))

    def __getitem__(self, index:int):
        """Generate one batch of data
        :param index: index of the batch
        :return: X and y when fitting. X only when predicting
        """
        self.seed += int(index) * self.epochNum

        # Generate indexes of the batch
        indexes = self.indexes[index * self.batch_size:(index + 1) * self.batch_size]

        # Find list of IDs
        list_IDs_temp = [self.list_IDs[k] for k in indexes]

        # Generate data
        X = self._generate_X(list_IDs_temp)

        if self.to_fit:
            Y = self._generate_y(list_IDs_temp)

            if self.augmentation is not None:

                random.seed(self.seed)
                xStack = np.stack([
                    self.augmentation(image=x)["image"] for x in X
                ], axis=0).astype(np.float32)

                random.seed(self.seed)
                yStack = np.stack([
                    self.augmentation(image=y)["image"] for y in Y
                ], axis=0).astype(np.float32)

                return xStack, yStack

            return X, Y
        else:
            return X

    def on_epoch_end(self):
        """Updates indexes after each epoch
        """
        self.epochNum += 1

        self.indexes = np.arange(len(self.list_IDs))
        if self.shuffle == True:
            np.random.shuffle(self.indexes)

    def _generate_X(self, list_IDs_temp):
        """Generates data containing batch_size images
        :param list_IDs_temp: list of label ids to load
        :return: batch of images
        """
        # Initialization
        X = np.empty((self.batch_size, *self.dim, self.input_channels))

        # Generate data
        for i, ID in enumerate(list_IDs_temp):
            # Store sample
            X[i,] = self._load_image(self.image_path + ID, self.input_image_type)
        return X

    def _generate_y(self, list_IDs_temp):
        """Generates data containing batch_size masks
        :param list_IDs_temp: list of label ids to load
        :return: batch if masks
        """
        y = np.empty((self.batch_size, *self.dim, self.output_channels), dtype=float)

        # Generate data
        for i, ID in enumerate(list_IDs_temp):
            # Store sample
            filename = ID.replace('_c', '_depth_vi')
            img = self._load_image(self.label_path + filename, self.output_image_type)
            img = img.reshape(*self.dim, self.output_channels)

            y[i,] = img

        return y

    def _load_image(self, image_path, image_type):
        """Load grayscale image
        :param image_path: path to image to load
        :return: loaded image
        """
        img = cv2.imread(image_path, image_type)
        img = img / 255.0
        return img