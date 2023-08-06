import unittest

import numpy as np
from joblib import Parallel, delayed
from tensorflow import keras

from tf2_vgpu.virtual_gpu import VirtualGPU


class TestVirtualGPU(unittest.TestCase):

    @staticmethod
    def _tf_job():
        gpu = VirtualGPU(512)

        x = np.random.rand(500, 20)
        y = np.random.randint(0, 1, size=(500, 1))

        input_layer = keras.layers.Input(shape=(20,))
        fc_1 = keras.layers.Dense(10)(input_layer)
        output_layer = keras.layers.Dense(1, activation='softmax')(fc_1)

        mod = keras.Model(inputs=input_layer, outputs=output_layer)
        mod.compile(optimizer='adam', loss='binary_crossentropy')

        mod.fit(x, y, epochs=10)

        return mod.predict(x)

    def test_in_joblib_parallel_single_job(self):
        # Arrange
        pool = Parallel(n_jobs=1)
        jobs = (delayed(self._tf_job)() for _ in range(5))

        # Act
        preds = pool(jobs)

        # Assert
        self.assertIsNotNone(preds)

    def test_in_joblib_parallel_multiple_job(self):
        # Arrange
        pool = Parallel(n_jobs=5)
        jobs = (delayed(self._tf_job)() for _ in range(5))

        # Act
        preds = pool(jobs)

        # Assert
        self.assertIsNotNone(preds)
