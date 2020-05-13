import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, GlobalAveragePooling2D, LeakyReLU, BatchNormalization, Conv2DTranspose

class DecoderNet:

    def Build(self, input):

        x = Conv2DTranspose(320, (5, 5), strides=(1, 1), padding='same', use_bias=False)(input)
        x = BatchNormalization()(x)
        x = LeakyReLU()(x)
        x = Conv2DTranspose(320, (3, 3), strides=(1, 1), padding='same', use_bias=False)(x)
        x = BatchNormalization()(x)

        x = Conv2DTranspose(240, (5, 5), strides=(2,2), padding='same', use_bias=False)(x)
        x = BatchNormalization()(x)
        x = LeakyReLU()(x)
        x = Conv2DTranspose(240, (3, 3), strides=(1, 1), padding='same', use_bias=False)(x)
        x = BatchNormalization()(x)

        x = Conv2DTranspose(120, (5, 5), strides=(2,2), padding='same', use_bias=False)(x)
        x = BatchNormalization()(x)
        x = LeakyReLU()(x)
        x = Conv2DTranspose(120, (3, 3), strides=(1, 1), padding='same', use_bias=False)(x)
        x = BatchNormalization()(x)

        x = Conv2DTranspose(60, (5, 5), strides=(2,2), padding='same', use_bias=False)(x)
        x = BatchNormalization()(x)
        x = LeakyReLU()(x)
        x = Conv2DTranspose(60, (3, 3), strides=(1, 1), padding='same', use_bias=False)(x)
        x = BatchNormalization()(x)

        x = Conv2DTranspose(32, (5, 5), strides=(2,2), padding='same', use_bias=False)(x)
        x = BatchNormalization()(x)
        x = LeakyReLU()(x)
        x = Conv2DTranspose(32, (3, 3), strides=(1, 1), padding='same', use_bias=False)(x)
        x = BatchNormalization()(x)

        x = Conv2DTranspose(1, (5, 5), strides=(2, 2), padding='same', use_bias=False)(x)

        #model = Model(inputs, x)

        return x

def CheckModelStructure():
    inputs = Input(shape=(4, 4, 320))

    decoder = DecoderNet()
    model = Model(inputs, decoder.Build(inputs))
    print(model.summary())

if __name__ == '__main__':
    CheckModelStructure()