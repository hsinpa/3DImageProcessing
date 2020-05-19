import tensorflow as tf
import numpy as np

from tensorflow.keras.layers import Conv2D, Input, Flatten, Dropout, Dense
from tensorflow.keras.models import Model

randomDataSet = np.random.rand(3, 128, 128)
randomOutputSet = np.random.rand(1, 128, 128)

# print(randomDataSet.shape)
# print(randomLabelSet.shape)
# onnx.
class SimpleNetworkUnity:

    def SetUp(self):

        inputs = Input(shape=(128, 128, 3), name='input_1')
        x = Conv2D(filters=8, kernel_size=3, strides=2, padding='same')(inputs)
        x = Dense(24, activation='relu')(x)
        x = tf.keras.layers.Dropout(0.2)(x)
        x = tf.keras.layers.Flatten()(x)
        x = tf.keras.layers.Dense(3)(x)

        return x, inputs
        # Conv2D(input_shape=(128, 128, 3), filters=8, kernel_size=3, strides=2, padding='same'),
        #     tf.keras.layers.Dense(24, activation='relu'),
        #     tf.keras.layers.Dropout(0.2),
        #     tf.keras.layers.Flatten(),
        #     tf.keras.layers.Dense(3)

    def Compile(self, input, model):

        loss_fn = tf.keras.losses.MeanSquaredError()

        self.model = Model(input, model)
        self.model.compile(optimizer='adam',
                      loss=loss_fn,
                      metrics=['accuracy'])
        print(self.model.summary())


    def Test(self, train_x, train_y):
        self.model.fit(train_x, train_y, epochs=5)

network = SimpleNetworkUnity()
output, input = network.SetUp()

network.Compile(input, output)

# randomDataSet = randomDataSet.reshape((-1, 128, 128, 3))
# randomOutputSet = randomOutputSet.reshape((-1, 128, 128, 1))
network.model.save("../save_model/", save_format="tf")

