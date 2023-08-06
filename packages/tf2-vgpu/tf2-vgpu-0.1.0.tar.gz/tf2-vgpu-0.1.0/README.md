# tf2-vgpu

Handle Tensorflow 2s experimental virtual GPU api to easily create multiple virtual GPUs on systems with (for now) 1 physical GPU, without breaking anything if run on a system without a GPU.
Useful for:
 - Quickly limiting GPU memory usage to avoid some out-of-memory error bugs, and to allow gaming while a model trains!  
 - Maximising GPU usage in parallel training where memory requirements are low and bottleneck is not gpu utilisation (eg. in [reinforcement learning](https://github.com/garethjns/reinforcement-learning-keras)). 
 
# Setup and Usage
````bash
pip install tf2-vgpu
````

```python 
from tf2_vgpu import VirtualGPU

VirtualGPU(128)

# Training code ...
```

## Example single job
Limits GPU memory, or does nothing if there's no GPU.

```python
import numpy as np
from tensorflow import keras

from tf2_vgpu import VirtualGPU

# Create virtual device with limited memory. 
# Returns flag indicating if GPU was created or not.
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
```

## Example parallel jobs
Limits GPU memory per process, or does nothing if there's no GPU.

```python
from tf2_vgpu import VirtualGPU
from joblib import Parallel, delayed
import numpy as np
from tensorflow import keras

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

# Simultaneously train a dummy model using joblib
x = np.random.rand(500, 20)
y = np.random.randint(0, 1, size=(500, 1))

jobs = (delayed(fit)(x, y) for _ in range(20))
preds = Parallel(n_jobs=5)(jobs)
```

The optimal number of simultaneous jobs varies depending on the model architecture, data size, and the system. For example 1 vs 5 jobs for this dummy model on with a 1080ti running in Windows doubles GPU utilisation:
1 job:
![1 job](https://raw.githubusercontent.com/garethjns/tf2-vgpu/master/images/1job.png) 

5 jobs:
![5 jobs](https://raw.githubusercontent.com/garethjns/tf2-vgpu/master/images/5jobs.png) 

## Example Scikit-learn compatible gridsearch
Limits GPU memory per process, or does nothing if there's no GPU.

```python
import numpy as np
from sklearn.base import BaseEstimator
from sklearn.model_selection import GridSearchCV
from tensorflow import keras

from tf2_vgpu import VirtualGPU


class NerualNetowrk(BaseEstimator):
    n_units: int
    n_epochs: int

    def __init__(self, n_units: int = 10, n_epochs: int = 10) -> None:
        self.set_params(n_units=n_units, n_epochs=n_epochs)

    def _build_model(self) -> None:
        input_layer = keras.layers.Input(shape=(20,))
        fc_1 = keras.layers.Dense(self.n_units)(input_layer)
        output_layer = keras.layers.Dense(1, activation='softmax')(fc_1)

        self.mod_ = keras.Model(inputs=input_layer, outputs=output_layer)

    def fit(self, x: np.ndarray, y: np.ndarray) -> "NerualNetowrk":
        # Create new GPU for each fit call
        VirtualGPU(128)

        self._build_model()
        self.mod_.compile(loss='binary_crossentropy')
        self.mod_.fit(x, y, epochs=self.n_epochs, verbose=False)

        return self

    def predict(self, x: np.ndarray) -> np.ndarray:
        return self.mod_.predict(x)

# Dummy data
x = np.random.rand(500, 20)
y = np.random.randint(0, 1, size=(500, 1))

# Run gridsearch
grid = GridSearchCV(estimator=NerualNetowrk(),
                    param_grid={'n_units': [8, 10, 12], 'n_epochs': [10, 20, 30]},
                    scoring='accuracy', n_jobs=5, verbose=10)
grid.fit(x, y)

# Predict from best model 
grid.best_estimator_.predict(x)
```

