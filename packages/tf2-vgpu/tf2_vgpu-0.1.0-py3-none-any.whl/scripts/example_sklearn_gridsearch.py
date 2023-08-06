import numpy as np
from sklearn.base import BaseEstimator
from sklearn.model_selection import GridSearchCV
from tensorflow import keras

from tf2_vgpu import VirtualGPU


class NerualNetowrk(BaseEstimator):
    n_units: int
    n_epochs: int

    def __init__(self, n_units: int = 10, n_epochs: int = 10) -> None:
        self.set_params(n_units=n_units,
                        n_epochs=n_epochs)

    def _build_model(self) -> None:
        input_layer = keras.layers.Input(shape=(20,))
        fc_1 = keras.layers.Dense(self.n_units)(input_layer)
        output_layer = keras.layers.Dense(1, activation='softmax')(fc_1)

        self.mod_ = keras.Model(inputs=input_layer, outputs=output_layer)

    def fit(self, x: np.ndarray, y: np.ndarray) -> "NerualNetowrk":
        VirtualGPU(128)

        self._build_model()
        self.mod_.compile(loss='binary_crossentropy')
        self.mod_.fit(x, y, epochs=self.n_epochs, verbose=False)

        return self

    def predict(self, x: np.ndarray) -> np.ndarray:
        return self.mod_.predict(x)


if __name__ == "__main__":
    x = np.random.rand(500, 20)
    y = np.random.randint(0, 1, size=(500, 1))

    grid = GridSearchCV(estimator=NerualNetowrk(),
                        param_grid={'n_units': [8, 10, 12],
                                    'n_epochs': [10, 20, 30]},
                        scoring='accuracy', n_jobs=5,
                        verbose=10)

    grid.fit(x, y)

    grid.best_estimator_.predict(x)
