from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2D, AvgPool2D, MaxPool2D
from tensorflow.keras.layers import Activation, BatchNormalization, concatenate, LeakyReLU
from tensorflow.keras.layers import Add, BatchNormalization, UpSampling2D, DepthwiseConv2D, add
import tensorflow as tf
from tensorflow.keras import backend as K

class ResidualNet:

    def relu6(self, x):
        """Relu 6
        """
        return K.relu(x, max_value=6.0)


    def transition_layer(self, x, f, maintain_filter=False):
        filtersize = f if maintain_filter else f // 2
        x = self._conv_block(x, filtersize, 3, 1)
        x = UpSampling2D(size=2,interpolation='bilinear')(x)
        return x

    def _conv_block(self, inputs, filters, kernel, strides):
        """Convolution Block
        This function defines a 2D convolution operation with BN and relu6.
        # Arguments
            inputs: Tensor, input tensor of conv layer.
            filters: Integer, the dimensionality of the output space.
            kernel: An integer or tuple/list of 2 integers, specifying the
                width and height of the 2D convolution window.
            strides: An integer or tuple/list of 2 integers,
                specifying the strides of the convolution along the width and height.
                Can be a single integer to specify the same value for
                all spatial dimensions.
        # Returns
            Output tensor.
        """

        channel_axis = 1 if K.image_data_format() == 'channels_first' else -1

        x = Conv2D(filters, kernel, padding='same', strides=strides)(inputs)
        x = BatchNormalization(axis=channel_axis)(x)
        return Activation(self.relu6)(x)

    def _bottleneck(self, inputs, filters, kernel, t, alpha, s, r=False):
        """Bottleneck
        This function defines a basic bottleneck structure.
        # Arguments
            inputs: Tensor, input tensor of conv layer.
            filters: Integer, the dimensionality of the output space.
            kernel: An integer or tuple/list of 2 integers, specifying the
                width and height of the 2D convolution window.
            t: Integer, expansion factor.
                t is always applied to the input size.
            s: An integer or tuple/list of 2 integers,specifying the strides
                of the convolution along the width and height.Can be a single
                integer to specify the same value for all spatial dimensions.
            alpha: Integer, width multiplier.
            r: Boolean, Whether to use the residuals.
        # Returns
            Output tensor.
        """

        channel_axis = 1 if K.image_data_format() == 'channels_first' else -1
        # Depth
        tchannel = K.int_shape(inputs)[channel_axis] * t
        # Width
        cchannel = int(filters * alpha)

        x = self._conv_block(inputs, tchannel, (1, 1), (1, 1))

        x = DepthwiseConv2D(kernel, strides=(s, s), depth_multiplier=1, padding='same')(x)
        x = BatchNormalization(axis=channel_axis)(x)
        x = Activation(self.relu6)(x)

        x = Conv2D(cchannel, (1, 1), strides=(1, 1), padding='same')(x)
        x = BatchNormalization(axis=channel_axis)(x)

        if r:
            x = Add()([x, inputs])

        return x

    def _inverted_residual_block(self, inputs, filters, kernel, t, alpha, strides, n):
        """Inverted Residual Block
        This function defines a sequence of 1 or more identical layers.
        # Arguments
            inputs: Tensor, input tensor of conv layer.
            filters: Integer, the dimensionality of the output space.
            kernel: An integer or tuple/list of 2 integers, specifying the
                width and height of the 2D convolution window.
            t: Integer, expansion factor.
                t is always applied to the input size.
            alpha: Integer, width multiplier.
            s: An integer or tuple/list of 2 integers,specifying the strides
                of the convolution along the width and height.Can be a single
                integer to specify the same value for all spatial dimensions.
            n: Integer, layer repeat times.
        # Returns
            Output tensor.
        """
        x = self._bottleneck(inputs, filters, kernel, t, alpha, strides)

        for i in range(1, n):
            x = self._bottleneck(x, filters, kernel, t, alpha, 1, True)

        return x

    def Build(self, x, encode_layer: []):
        # x = UpSampling2D(size=2,interpolation='bilinear')(x)
        # x = Conv2D(96, kernel_size=3, strides=1, padding='same')(x)

        alpha = 1
        denseSetup = [(4, 160, 96), (6, 64, 32), (12, 28,24), (6, 20, 16)]
        denseSetCount = len(denseSetup)
        for i in range(denseSetCount):
            r, train_f, trans_f = denseSetup[i]

            x = self._inverted_residual_block(x, filters=train_f, kernel=3, strides=1, n=r, alpha=alpha, t=6)
            x = self.transition_layer(x, trans_f, maintain_filter=True)
            if encode_layer is not None:
                x = Add()([x, encode_layer[denseSetCount - i - 1]])

        x = self._inverted_residual_block(x, filters=8, kernel=3, strides=1, t=3, n=2, alpha=alpha)
        x = self.transition_layer(x, 8, maintain_filter=True)

        # x = LeakyReLU(alpha=0.2)(x)
        x = Conv2D(filters=1, kernel_size=9, strides=1, padding='same', name='output_1')(x)

        return x

def CheckModelStructure():
    tf.keras.backend.set_image_data_format('channels_last')

    inputs = Input(shape=(4, 4, 320))

    denseNet = ResidualNet()
    output = denseNet.Build(inputs, None)
    model = Model(inputs, output)

    print(model.summary())

if __name__ == '__main__':
    CheckModelStructure()