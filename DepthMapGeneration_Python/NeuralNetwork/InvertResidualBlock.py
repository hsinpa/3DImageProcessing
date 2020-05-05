import tensorflow as tf
from tensorflow.keras.layers import Layer, Conv2D, DepthwiseConv2D, BatchNormalization

class InvertedResidual(Layer):
    def __init__(self, filters, strides, expansion_factor=6, trainable=True, name=None, **kwargs):
        super(InvertedResidual, self).__init__(trainable=trainable, name=name, **kwargs)
        self.filters = filters
        self.strides = strides
        self.expansion_factor = expansion_factor	# allowed to be decimal value

    def build(self, input_shape):
        input_channels = int(input_shape[3])
        self.ptwise_conv1 = Conv2D(filters=int(input_channels*self.expansion_factor), kernel_size=1, use_bias=False)
        self.dwise = DepthwiseConv2D(kernel_size=3, strides=self.strides, padding='same', use_bias=False)
        self.ptwise_conv2 = Conv2D(filters=self.filters, kernel_size=1, use_bias=False)

        self.bn1 = BatchNormalization()
        self.bn2 = BatchNormalization()
        self.bn3 = BatchNormalization()

    def call(self, input_x):
        # Expansion to high-dimensional space
        x = self.ptwise_conv1(input_x)
        x = self.bn1(x)
        x = tf.nn.relu6(x)

        # Spatial filtering
        x = self.dwise(x)
        x = self.bn2(x)
        x = tf.nn.relu6(x)

        # Projection back to low-dimensional space w/ linear activation
        x = self.ptwise_conv2(x)
        x = self.bn3(x)

        # Residual connection if i/o have same spatial and depth dims
        if input_x.shape[1:] == x.shape[1:]:
            x += input_x
        return x

    def get_config(self):
        cfg = super(InvertedResidual, self).get_config()
        cfg.update({'filters': self.filters,
        	        'strides': self.strides,
        	        'expansion_factor': self.expansion_factor})
        return cfg