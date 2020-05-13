from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Input, LeakyReLU, Flatten, PReLU, UpSampling2D, BatchNormalization, Conv2D
from tensorflow.keras.models import Model
from tensorflow.keras.layers import add

class SRGANDecoder:
    def res_block_gen(self, model, kernal_size, filters, strides):
        gen = model

        model = Conv2D(filters=filters, kernel_size=kernal_size, strides=strides, padding="same")(model)
        model = BatchNormalization(momentum=0.5)(model)
        # Using Parametric ReLU
        model = PReLU(alpha_initializer='zeros', alpha_regularizer=None, alpha_constraint=None, shared_axes=[1, 2])(
            model)
        model = Conv2D(filters=filters, kernel_size=kernal_size, strides=strides, padding="same")(model)
        model = BatchNormalization(momentum=0.5)(model)

        model = add([gen, model])

        return model

    def up_sampling_block(self, model, kernal_size, filters, strides):
        # In place of Conv2D and UpSampling2D we can also use Conv2DTranspose (Both are used for Deconvolution)
        # Even we can have our own function for deconvolution (i.e one made in Utils.py)
        # model = Conv2DTranspose(filters = filters, kernel_size = kernal_size, strides = strides, padding = "same")(model)
        model = Conv2D(filters=filters, kernel_size=kernal_size, strides=strides, padding="same")(model)
        model = UpSampling2D(size=2)(model)
        model = LeakyReLU(alpha=0.2)(model)

        return model

    def Build(self, input):

        model = Conv2D(filters=64, kernel_size=9, strides=1, padding="same")(input)
        model = PReLU(alpha_initializer='zeros', alpha_regularizer=None, alpha_constraint=None, shared_axes=[1, 2])(
            model)

        gen_model = model

        # Using 16 Residual Blocks
        for index in range(2):
            model = self.res_block_gen(model, 3, 64, 1)

        model = Conv2D(filters=64, kernel_size=3, strides=1, padding="same")(model)
        model = BatchNormalization(momentum=0.5)(model)
        model = add([gen_model, model])

        # Using 2 UpSampling Blocks
        for index in range(5):
            model = self.up_sampling_block(model, 3, 256, 1)

        model = Conv2D(filters=1, kernel_size=9, strides=1, padding="same" )(model)

        return model

def CheckModelStructure():
    inputs = Input(shape=(4, 4, 320))

    decoder = SRGANDecoder()
    model = Model(inputs, decoder.Build(inputs))
    print(model.summary())

if __name__ == '__main__':
    CheckModelStructure()