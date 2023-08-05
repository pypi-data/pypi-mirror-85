import torch as T
from lpd.metrics.metric_base import MetricBase


class ConfusionMatrix(MetricBase):
    def __init__(self, threshold=0.5):
        self.tp = 0
        self.tn = 0
        self.fp = 0
        self.fp = 0

    def __call__(self, y_pred: T.Tensor, y_true: T.Tensor):
        assert y_true.size() == y_pred.size()
        pred = y_pred.round().long()
        accuracy = pred.eq(y_true).float().sum() / y_true.numel()
        return accuracy


