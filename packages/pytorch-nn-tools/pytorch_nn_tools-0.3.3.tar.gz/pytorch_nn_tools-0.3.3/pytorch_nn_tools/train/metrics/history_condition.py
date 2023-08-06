from typing import Callable, Dict


class HistoryCondition:
    def __init__(self, metric_name: str, history_condition: Callable, history=()):
        """
        The class aggregates the history of metrics and implements a condition on one of the metrics

        >>> hc = HistoryCondition("accuracy", lambda hist: len(hist) < 2 or hist[-1] > max(hist[:-1]))
        >>> assert hc({"accuracy": 0.10, "precision": 0.5}) is True
        >>> assert hc({"accuracy": 0.08, "precision": 0.6}) is False
        >>> assert hc({"accuracy": 0.09, "precision": 0.7}) is False
        >>> assert hc({"accuracy": 0.11, "precision": 0.8}) is True
        """
        self.metric_name = metric_name
        self.history = list(history[:])
        self.condition = history_condition

    def __call__(self, metrics: Dict):
        self.history.append(metrics[self.metric_name])
        result = self.condition(self.history[:])
        return result
