# Torch-metrics: model evaluation metrics for PyTorch
[![PyPI version](https://badge.fury.io/py/torch-metrics.svg)](https://badge.fury.io/py/torch-metrics)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

As summarized in this [issue](https://github.com/pytorch/pytorch/issues/22439), Pytorch does not have a built-in libary `torch.metrics` for model evaluation metrics. This python library serves as a custom library to provide common evaluation metrics in Pytorch, similar to `tf.keras.metrics`. This is similar to the metrics library in [PyTorch Lightning](https://pytorch-lightning.readthedocs.io/en/latest/metrics.html#class-metrics).

### Usage

- `pip install --upgrade torch-metrics` or 
- `git clone https://github.com/enochkan/torch-metrics.git`

```python
from torch_metrics import Accuracy

## define metric ##
metric = Accuracy(from_logits=False)
y_pred = torch.tensor([1, 2, 3, 4])
y_true = torch.tensor([0, 2, 3, 4])

print(metric(y_pred, y_true))
```

```python
from torch_metrics import Accuracy

## define metric ##
metric = Accuracy()
y_pred = torch.tensor([[0.2, 0.6, 0.1, 0.05, 0.05],
                       [0.2, 0.1, 0.6, 0.05, 0.05],
                       [0.2, 0.05, 0.1, 0.6, 0.05],
                       [0.2, 0.05, 0.05, 0.05, 0.65]])
y_true = torch.tensor([0, 2, 3, 4])

print(metric(y_pred, y_true))
```

### Implementation

Metrics from `tf.keras.metrics` and other metrics that are already implemented vs to-do

- [X] MeanSquaredError class
- [X] RootMeanSquaredError class
- [X] MeanAbsoluteError class
- [X] Precision class
- [X] Recall class
- [X] MeanIoU class
- [X] DSC class (Dice Similarity Coefficient)
- [X] F1Score class
- [X] RSquared class
- [X] Hinge class
- [X] SquaredHinge class
- [X] LogCoshError class
- [X] Accuracy class
- [X] KLDivergence class
- [ ] CosineSimilarity class
- [ ] AUC class
- [ ] BinaryCrossEntropy class
- [ ] CategoricalCrossEntropy class
- [ ] SparseCategoricalCrossentropy class


Please raise issues or feature requests [here](https://github.com/enochkan/torch-metrics/issues). 
