from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2D, AvgPool2D, MaxPool2D
from tensorflow.keras.layers import Activation, BatchNormalization, concatenate, LeakyReLU
from tensorflow.keras.layers import Add, BatchNormalization, UpSampling2D, PReLU

from tensorflow.keras import backend as K

class DenseNet:

    def __init__(self, default_filter=32):
        self.f = default_filter

    def relu6(self, x):
        """Relu 6
        """
        return K.relu(x, max_value=6.0)

    def bn_rl_conv(self, x, f, k=1, s=1):
        x = BatchNormalization()(x)
        x = LeakyReLU(alpha=0.2)(x)
        x = Conv2D(f, kernel_size=k, strides=s, padding='same')(x)
        return x

    def dense_block(self, x, f, t):
        for i in range(t):
            y = self.bn_rl_conv(x, f*4)
            y = self.bn_rl_conv(y, f, k=3)
            x = concatenate([y, x], axis=3)
        return x

    def transition_layer(self, x, f, maintain_filter=False):
        filtersize = f if maintain_filter else f // 2
        x = self.bn_rl_conv(x, filtersize)
        x = UpSampling2D(size=2,interpolation='bilinear')(x)
        return x

    def Build(self, x, encode_layer: []):
        # x = UpSampling2D(size=2,interpolation='bilinear')(x)
        # x = Conv2D(96, kernel_size=3, strides=1, padding='same')(x)

        denseSetup = [(6, 96), (8, 32), (14, 24), (8, 16)]
        denseSetCount = len(denseSetup)
        for i in range(denseSetCount):
            r, f = denseSetup[i]
            x = self.dense_block(x, self.f, r)
            x = self.transition_layer(x, f, maintain_filter=True)
            if encode_layer is not None:
                x = Add()([x, encode_layer[denseSetCount - i - 1]])

        x = self.dense_block(x, self.f, 3)
        x = self.transition_layer(x, 8, maintain_filter=True)

        # x = LeakyReLU(alpha=0.2)(x)
        x = Conv2D(filters=1, kernel_size=9, strides=1, padding='same')(x)

        return x

def CheckModelStructure():
    inputs = Input(shape=(4, 4, 320))

    denseNet = DenseNet(default_filter=32)
    output = denseNet.Build(inputs, None)
    model = Model(inputs, output)

    print(model.summary())

if __name__ == '__main__':
    CheckModelStructure()