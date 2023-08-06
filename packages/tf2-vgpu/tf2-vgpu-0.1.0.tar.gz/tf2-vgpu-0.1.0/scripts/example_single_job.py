import numpy as np
from tensorflow import keras

from tf2_vgpu import VirtualGPU

if __name__ == "__main__":
    # Create virtual device with limited memory
    gpu = VirtualGPU(128)

    # Create and train a dummy model
    x = np.random.rand(500, 20)
    y = np.random.randint(0, 1, size=(500, 1))

    input_layer = keras.layers.Input(shape=(20,))
    fc_1 = keras.layers.Dense(10)(input_layer)
    output_layer = keras.layers.Dense(1, activation='softmax')(fc_1)

    mod = keras.Model(inputs=input_layer, outputs=output_layer)
    mod.compile(optimizer='adam', loss='binary_crossentropy')

    mod.fit(x, y, epochs=10)
