import numpy as np
from joblib import Parallel, delayed
from tensorflow import keras

from tf2_vgpu import VirtualGPU


# Define pickle-compatible training function
# This could be method of an sklearn compatible object for use with grid search
def fit(x, y):
    # Create virtual device with limited memory, just for this model
    VirtualGPU(128)

    input_layer = keras.layers.Input(shape=(20,))
    fc_1 = keras.layers.Dense(10)(input_layer)
    output_layer = keras.layers.Dense(1, activation='softmax')(fc_1)

    mod = keras.Model(inputs=input_layer, outputs=output_layer)
    mod.compile(optimizer='adam', loss='binary_crossentropy')

    mod.fit(x, y, epochs=100)

    return mod.predict(x)


if __name__ == "__main__":
    # Simultaneously train a dummy model using joblib
    x = np.random.rand(500, 20)
    y = np.random.randint(0, 1, size=(500, 1))

    jobs = (delayed(fit)(x, y) for _ in range(20))
    preds = Parallel(n_jobs=5)(jobs)
