import numpy as np
import tensorflow as tf
import tensorflow.keras.backend as K
import NeuralNetwork.MobileNetV3
from NeuralNetwork.DecoderNet import DecoderNet
from NeuralNetwork.SRGANDecoder import SRGANDecoder
from NeuralNetwork.PretrainedModel import PretrainedModel
from tensorflow.keras.layers import  Concatenate, Add
from NeuralNetwork.MobileNetV3 import MobileNetv3
from tensorflow.keras.models import Model
from DataLoader.DataPreparator import DataPreparator
from DataLoader.ImageDataLoader import ImageDataLoader
import cv2
import matplotlib.pyplot as plt
import os
from DataLoader.LoaderUtility import  LoaderUtility
from NeuralNetwork.LossFunction import depth_loss_function
import random
import time

# os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
from albumentations import (
    Compose, HorizontalFlip, Blur, RandomGamma
)
dataLoader = LoaderUtility()
EPOCHS = 100
BATCHSIZE = 16
trainXPath = '../Dataset/ResizeImage/Train/Raw/'
trainYPath = '../Dataset/ResizeImage/Train/Depth/'

validXPath = '../Dataset/ResizeImage/Validation/Raw/'
validYPath = '../Dataset/ResizeImage/Validation/Depth/'

trainData = dataLoader.GetFileNameFromPath(trainXPath)
validData = dataLoader.GetFileNameFromPath(validXPath)

startSeed = (time.time())

AUGMENTATIONS_TRAIN = Compose([
    HorizontalFlip(p=0.5),
    RandomGamma(gamma_limit=(80, 120), p=0.1),
    RandomGamma(p=0.1)
])

trainDataLoader = ImageDataLoader(trainData, trainXPath, trainYPath, batch_size=BATCHSIZE, dim=(128, 128), input_channels=3,
                                  output_channels=1, input_image_type=cv2.COLOR_BGR2RGB, output_image_type=cv2.IMREAD_GRAYSCALE,
                                  augmentation=AUGMENTATIONS_TRAIN, initSeed=startSeed)

validDataLoader = ImageDataLoader(validData, validXPath, validYPath, batch_size=1, dim=(128, 128), input_channels=3,
                                  output_channels=1, input_image_type=cv2.COLOR_BGR2RGB, output_image_type=cv2.IMREAD_GRAYSCALE)


x , y = trainDataLoader.__getitem__(5)

cv2.imshow('input',x[10])
cv2.imshow('groundTruth', y[10])

cv2.waitKey(0)
cv2.destroyAllWindows()

# dataPreparator = DataPreparator(xPath, cv2.COLOR_BGR2RGB, yPath, cv2.IMREAD_GRAYSCALE)
# trainXSet, trainYSet, testXSet, testYSet = dataPreparator.GetTrainTestSet(ratio=0.05, useAugmentation=False)
#
# # print(trainXSet.shape)
# trainYSet = trainYSet.reshape(len(trainYSet), 128, 128, 1)
# testYSet = testYSet.reshape(len(testYSet), 128, 128, 1)
#
# #mobileDepthNet = MobileDepthNet()
# mobileDepthNet = PretrainedModel()
# model = mobileDepthNet.Build((128,128,3))
#
# checkpoint_path = "../save_model/training_1/cp.ckpt"
# checkpoint_dir = os.path.dirname(checkpoint_path)

# Create a callback that saves the model's weights
# cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
#                                                  save_weights_only=True,
#                                                  verbose=1)
# if os.path.exists(checkpoint_path + '.index'):
#     model.load_weights(checkpoint_path)

#model_history = model.fit(x=trainDataLoader, epochs=EPOCHS, callbacks=[cp_callback], validation_data=validDataLoader)

# predictSet = trainXSet[0].reshape(1, 128, 128, 3)
# result = model.predict(predictSet)
#
# input = trainXSet[0].reshape(128, 128, 3)
# result = result.reshape(128, 128, 1)
# groundTruth = trainYSet[0].reshape(128,128,1)
#
# print(result)
# print(groundTruth)
#
# cv2.imshow('image',result)
# cv2.imshow('input',input)
# cv2.imshow('groundTruth', groundTruth)
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()
