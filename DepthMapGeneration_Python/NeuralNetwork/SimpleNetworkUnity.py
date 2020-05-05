import tensorflow as tf
import numpy as np
import mlagents.trainers.tensorflow_to_barracuda as barracuda
import tf2onnx.convert as onnx

randomDataSet = np.random.rand(3, 12, 12)
randomLabelSet = np.array([1, 2, 3])

# print(randomDataSet.shape)
# print(randomLabelSet.shape)
# onnx.
class SimpleNetworkUnity:

    def SetUp(self):
        self.model = tf.keras.models.Sequential([
            tf.keras.layers.Flatten(input_shape=(12, 12)),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(1)
        ])

    def Test(self, train_x, train_y):
        loss_fn = tf.keras.losses.MeanSquaredError()

        self.model.compile(optimizer='adam',
                      loss=loss_fn,
                      metrics=['accuracy'])

        self.model.fit(train_x, train_y, epochs=5)

network = SimpleNetworkUnity()
network.SetUp()
network.Test(randomDataSet, randomLabelSet)
network.model.save("../save_model/", save_format="tf")
