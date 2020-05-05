import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, GlobalAveragePooling2D, LeakyReLU, BatchNormalization, Conv2DTranspose

class DecoderNet:

    def Build(self, input):

        x = Conv2DTranspose(320, (5, 5), strides=(1, 1), padding='same', use_bias=False)(input)
        x = BatchNormalization()(x)
        x = LeakyReLU()(x)

        x = Conv2DTranspose(160, (5, 5), strides=(2,2), padding='same', use_bias=False)(x)
        x = BatchNormalization()(x)
        x = LeakyReLU()(x)

        x = Conv2DTranspose(96, (5, 5), strides=(2,2), padding='same', use_bias=False)(x)
        x = BatchNormalization()(x)
        x = LeakyReLU()(x)

        x = Conv2DTranspose(64, (5, 5), strides=(2, 2), padding='same', use_bias=False)(x)
        x = BatchNormalization()(x)
        x = LeakyReLU()(x)

        x = Conv2DTranspose(32, (5, 5), strides=(2, 2), padding='same', use_bias=False)(x)
        x = BatchNormalization()(x)
        x = LeakyReLU()(x)

        x = Conv2DTranspose(1, (5, 5), strides=(2, 2), padding='same', use_bias=False, activation='sigmoid')(x)

        #model = Model(inputs, x)

        return x

def CheckModelStructure():
    inputs = Input(shape=(8, 8, 320))

    decoder = DecoderNet()
    model = Model(inputs, decoder.Build(inputs))
    print(model.summary())

if __name__ == '__main__':
    CheckModelStructure()