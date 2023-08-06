from decimal import Decimal
from typing import Union

from celery_progress.backend import PROGRESS_STATE, AbstractProgressRecorder


class ProgressRecorder(AbstractProgressRecorder):
    def __init__(self, task):
        self.task = task
        self.messages = []
        self.total = 100
        self.current = 0

    def set_progress(self, current: Union[int, float], **kwargs):
        self.current = current

        percent = 0
        if self.total > 0:
            percent = (Decimal(current) / Decimal(self.total)) * Decimal(100)
            percent = float(round(percent, 2))

        self.task.update_state(
            state=PROGRESS_STATE,
            meta={
                "current": current,
                "total": self.total,
                "percent": percent,
                "messages": self.messages,
            },
        )

    def add_message(self, level: int, message: str, **kwargs):
        self.messages.append((level, message))
        self.set_progress(self.current)
