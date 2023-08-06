from typing import List

from .flavor import (
    KerasModelFlavor,
    LightGBMModelFlavor,
    ModelFlavor,
    PyTorchModelFlavor,
    ScikitLearnModelFlavor,
    SparkMLModelFlavor,
    TensorFlowModelFlavor,
    XGBoostModelFlavor,
)


MODEL_FLAVORS: List[ModelFlavor] = [
    SparkMLModelFlavor(),
    ScikitLearnModelFlavor(),
    PyTorchModelFlavor(),
    XGBoostModelFlavor(),
    LightGBMModelFlavor(),
    KerasModelFlavor(),
    TensorFlowModelFlavor(),
]
