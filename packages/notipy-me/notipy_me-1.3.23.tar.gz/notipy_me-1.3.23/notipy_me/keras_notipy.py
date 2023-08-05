from typing import Dict
from sanitize_ml_labels import sanitize_ml_labels
from .notipy_me import Notipy

try:
    from tensorflow.keras.callbacks import Callback
except ModuleNotFoundError:
    pass
else:
    class KerasNotipy(Callback):

        def __init__(
            self,
            task_name: str = None,
            metadata: Dict = None,
            report_only_validation: bool = True,
            sanitize_metrics: bool = True
        ):
            """Create new Keras Notipy object.

            Parameters
            -----------------
            task_name: str = None,
                Optional name of the task to use for report.
            metadata: Dict = None,
                Optional metadata to be reported alongside data.
            report_only_validation: bool = True,
                Report only metrics relative to the validation set.
                If the log only contains metrics relative to the training,
                this limitation is automatically lifted.
            sanitize_metrics: bool = True,
                Sanitize the names of the metrics.
            """
            super().__init__()
            self._metadata = {} if metadata is None else metadata
            self._notipy = Notipy(task_name=task_name)
            self._report_only_validation = report_only_validation
            self._sanitize_metrics = sanitize_metrics

        def on_train_begin(self, logs=None):
            """Start notipy as the training begins."""
            self._notipy.enter()

        def on_epoch_end(self, epoch: int, logs=None):
            """When the epoch ends we report how the model is doing."""
            if logs is not None:
                log_has_validation = any(
                    metric.startswith("val")
                    for metric in logs
                )
                self._notipy.add_report({
                    **self._metadata,
                    **{
                        sanitize_ml_labels(metric) if self._sanitize_metrics else metric: value
                        for metric, value in logs.items()
                        if not self._report_only_validation or metric.startswith("val") or not log_has_validation
                    },
                    "epoch": epoch
                })

        def on_train_end(self, logs=None):
            """When the training is complete we close down also the Notipy."""
            self._notipy.exit()
