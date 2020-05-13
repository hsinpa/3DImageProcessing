import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2D, GlobalAveragePooling2D, Dropout
from tensorflow.keras.layers import Activation, BatchNormalization, Add, Reshape, DepthwiseConv2D
from tensorflow.keras import backend as K
from NeuralNetwork.LossFunction import depth_loss_function
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2

class PretrainedModel:
    def Build(self, image_shape):
        outputShape = (image_shape[0], image_shape[1], 1)

        pretrainMobileNet = MobileNetV2(input_shape=image_shape, weights='imagenet', include_top=False, alpha=1.0)

        print(pretrainMobileNet.summary())

        # mobileNet, mobileInput = MobileNetv3(inputsStructure, 100)
        #
        # # decoder = DecoderNet()
        # # decoder = decoder.Build(mobileNet)
        #
        # decoder = SRGANDecoder()
        # decoder = decoder.Build(mobileNet)

        #model = Model(mobileInput, decoder)

        # merge = Concatenate()([mobileNetModel.output, decoderModel.output])
        #
        # model = Model(decoder, decoderInput)

        # adam = tf.keras.optimizers.Adam()
        #
        # model.compile(optimizer=adam,
        #               loss=depth_loss_function,
        #               metrics=[tf.keras.metrics.Accuracy()])
        #
        # print(model.summary())

        return pretrainMobileNet

if __name__ == '__main__':
    model = PretrainedModel()