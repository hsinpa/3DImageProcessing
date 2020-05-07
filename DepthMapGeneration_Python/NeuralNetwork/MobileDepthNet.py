import numpy as np
import tensorflow as tf
import tensorflow.keras.backend as K
import NeuralNetwork.MobileNetV3
from NeuralNetwork.DecoderNet import DecoderNet
from NeuralNetwork.SRGANDecoder import SRGANDecoder

from tensorflow.keras.layers import  Concatenate, Add
from NeuralNetwork.MobileNetV3 import MobileNetv3
from tensorflow.keras.models import Model
from DataLoader.DataPreparator import DataPreparator
import cv2
import matplotlib.pyplot as plt
import os
from DataLoader.LoaderUtility import  LoaderUtility
class MobileDepthNet:


    def dice_loss(self, y_true, y_pred):
        numerator = 2 * tf.reduce_sum(y_true * y_pred, axis=-1)
        denominator = tf.reduce_sum(y_true + y_pred, axis=-1)

        return 1 - (numerator + 1) / (denominator + 1)

    def jaccard_distance_loss(self,y_true, y_pred, smooth=100):
        """
        Jaccard = (|X & Y|)/ (|X|+ |Y| - |X & Y|)
                = sum(|A*B|)/(sum(|A|)+sum(|B|)-sum(|A*B|))

        The jaccard distance loss is usefull for unbalanced datasets. This has been
        shifted so it converges on 0 and is smoothed to avoid exploding or disapearing
        gradient.

        Ref: https://en.wikipedia.org/wiki/Jaccard_index

        @url: https://gist.github.com/wassname/f1452b748efcbeb4cb9b1d059dce6f96
        @author: wassname
        """
        intersection = K.sum(K.abs(y_true * y_pred), axis=-1)
        sum_ = K.sum(K.abs(y_true) + K.abs(y_pred), axis=-1)
        jac = (intersection + smooth) / (sum_ - intersection + smooth)
        return (1 - jac) * smooth


    def Build(self):
        inputsStructure = (128, 128, 1)
        mobilenetOutputStructure = (16, 16, 320)

        mobileNet, mobileInput = MobileNetv3(inputsStructure, 100)

        # decoder = DecoderNet()
        # decoder = decoder.Build(mobileNet)

        decoder = SRGANDecoder()
        decoder = decoder.Build(mobileNet)

        model = Model(mobileInput, decoder)

        # merge = Concatenate()([mobileNetModel.output, decoderModel.output])
        #
        # model = Model(decoder, decoderInput)

        adam = tf.keras.optimizers.Adam()

        model.compile(optimizer=adam,
                      loss=tf.keras.losses.MeanAbsoluteError(),
                      metrics=[tf.keras.metrics.Accuracy()])

        print(model.summary())

        return model

#os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

dataLoader = LoaderUtility()
EPOCHS = 20
BATCHSIZE = 16
xPath = '../Dataset/ResizeImage/Raw/'
yPath = '../Dataset/ResizeImage/Depth/'

dataPreparator = DataPreparator(xPath, cv2.COLOR_BGR2RGB, yPath, cv2.IMREAD_GRAYSCALE)
trainXSet, trainYSet, testXSet, testYSet = dataPreparator.GetTrainTestSet(ratio=0.05, useAugmentation=False)

# print(trainXSet.shape)
trainYSet = trainYSet.reshape(len(trainYSet), 128, 128, 1)
testYSet = testYSet.reshape(len(testYSet), 128, 128, 1)

mobileDepthNet = MobileDepthNet()
model = mobileDepthNet.Build()

checkpoint_path = "../save_model/training_1/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

# Create a callback that saves the model's weights
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)
if os.path.exists(checkpoint_path + '.index'):
    model.load_weights(checkpoint_path)

# model_history = model.fit(x = trainXSet, y= trainYSet, epochs=EPOCHS,batch_size=BATCHSIZE,
#                           shuffle=True, callbacks=[cp_callback],
#                           validation_data=(testXSet, testYSet))

# predictSet = trainXSet[0].reshape(1, 128, 128, 3)
# result = model.predict(predictSet)

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
#