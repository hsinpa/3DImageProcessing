import tensorflow as tf
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.layers import Input, Conv2D, GlobalAveragePooling2D, Dropout
from tensorflow.keras.layers import Activation, BatchNormalization, Add, Reshape, DepthwiseConv2D
from tensorflow.keras import backend as K
from NeuralNetwork.LossFunction import depth_loss_function
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2
from NeuralNetwork.NetworkUtility import getLayerIndexByName
from NeuralNetwork.SRGANDecoder import SRGANDecoder
from NeuralNetwork.MobileNetV3 import MobileNetv3
from NeuralNetwork.DenseNet import DenseNet
from NeuralNetwork.ResidualNet import ResidualNet

class PretrainedModel:
    def Build(self, image_shape, data_format='channels_last'):
        mobilenetv3, mobileInput, encode_layer = MobileNetv3(image_shape, 100, data_format=data_format)

        # pretrainMobileNet = MobileNetV2(input_shape=image_shape, weights='imagenet', include_top=False, alpha=1.0)
        #
        # targetIndex = getLayerIndexByName(pretrainMobileNet, 'block_4_expand')
        #
        # for layerIndex in range(targetIndex):
        #     pretrainMobileNet.layers[layerIndex].trainable = False
        #
        # mobilenetOutput = pretrainMobileNet.layers[-3].output

        decoder = ResidualNet()
        decoder = decoder.Build(mobilenetv3, encode_layer)

        # decoder = DenseNet(default_filter=32)
        # decoder = decoder.Build(mobilenetv3, encode_layer)
        model = Model(mobileInput, decoder)
        print(model.summary())

        adam = tf.keras.optimizers.Adam()

        model.compile(optimizer=adam,
        loss=depth_loss_function,
        metrics=[tf.keras.metrics.MeanSquaredLogarithmicError(), tf.keras.metrics.MeanSquaredError()])
        return model

if __name__ == '__main__':
    model = PretrainedModel()
    m = model.Build((128, 128, 3), data_format='channels_last')
    # m.save("../save_model/", save_format="tf")

