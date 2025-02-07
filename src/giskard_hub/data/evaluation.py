from __future__ import annotations

import time
from dataclasses import dataclass, field
from time import sleep
from typing import Any, Dict, List

from rich.console import Console
from rich.table import Table

from ._base import BaseData
from ._entity import Entity
from .conversation import Conversation
from .dataset import Dataset
from .model import Model, ModelOutput
from .task import TaskProgress, TaskStatus


@dataclass
class Metric(BaseData):
    """Evaluation metric.

    Attributes
    ----------
    name : str
        The name of the metric (e.g. "correctness").
    passed : int
        The number of samples that passed evaluations.
    failed : int
        The number of samples that failed evaluations.
    skipped: int
        The number of samples that were not evaluated (typically because of
        missing evaluation annotations).
    errored : int
        The number of samples that errored during evaluations.
    total : int
        The total number of samples (including the ones skipped).
    percentage : float
        The percentage of passed evaluations (not considering the skipped
        samples).
    """

    name: str
    passed: int
    failed: int
    errored: int
    total: int

    @property
    def skipped(self):
        return self.total - self.passed - self.failed - self.errored

    @property
    def percentage(self):
        tot = self.total - self.skipped
        if tot == 0:
            return float("nan")
        return self.passed / tot * 100


@dataclass
class EvaluationRun(Entity):
    """Evaluation run."""

    name: str | None = None
    project_id: str | None = None
    datasets: List[Dataset] = field(default_factory=list)
    model: Model | None = None
    criteria: List = field(default_factory=list)
    metrics: List[Metric] = field(default_factory=list)
    progress: TaskProgress | None = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs) -> "EvaluationRun":
        data = dict(data)
        data["datasets"] = [
            Dataset.from_dict(d, **kwargs) for d in data.get("datasets", [])
        ]
        data["model"] = Model.from_dict(data["model"], **kwargs)
        data["progress"] = TaskProgress.from_dict(data.get("status", {}))
        data["metrics"] = [Metric.from_dict(m) for m in data.get("metrics", [])]

        return super().from_dict(data, **kwargs)

    def refresh(self) -> EvaluationRun:
        """Refresh the evaluation run from the Hub."""
        if not self._client or not self.id:
            raise ValueError(
                "This evaluation run instance is detached or unsaved and cannot be refreshed."
            )

        data = self._client.evaluations.retrieve(self.id)
        self._hydrate(data)

        return self

    def is_running(self) -> bool:
        """Check if the evaluation is running."""
        return self.progress.status == TaskStatus.RUNNING

    def is_finished(self) -> bool:
        """Check if the evaluation is finished."""
        return self.progress.status == TaskStatus.FINISHED

    def is_errored(self) -> bool:
        """Check if the evaluation terminated with an error."""
        return self.progress.status == TaskStatus.ERROR

    def wait_for_completion(
        self, timeout: float = 600, poll_interval: float = 5
    ) -> EvaluationRun:
        """Wait for the evaluation to complete successfully.

        Parameters
        ----------
        timeout : int, optional
            The timeout in seconds, by default 600
        poll_interval : int, optional
            The polling interval in seconds, by default 5.

        Returns
        -------
        EvaluationRun
            The updated evaluation run instance. The object will have a valid
            ``metrics`` attribute containing the evaluation results.
        """
        end_time = time.perf_counter() + timeout
        if self.is_running():
            self.refresh()
        while time.perf_counter() < end_time:
            if not self.is_running():
                break
            sleep(poll_interval)
            self.refresh()

        if self.is_finished():
            return self

        if self.is_errored():
            raise RuntimeError("Evaluation failed")

        if self.is_running():
            raise TimeoutError("Evaluation did not finish in time.")

        raise RuntimeError("Evaluation was aborted.")

    def print_metrics(self):
        """Print the evaluation metrics."""
        console = Console()
        table = Table(
            "Metric",
            "Result",
            "Details",
            title=f"Evaluation Run [bold cyan]{self.name}[/bold cyan]",
        )
        for metric in self.metrics:
            if metric.percentage != metric.percentage:
                continue

            if metric.percentage > 80:
                color = "green"
            elif metric.percentage > 50:
                color = "yellow"
            else:
                color = "red"

            table.add_row(
                f"[bold]{metric.name.capitalize()}[/bold]",
                f"[{color}]{metric.percentage:.2f}%[/{color}]",
                f"[bright_black]{metric.passed} passed, {metric.failed} failed, {metric.errored} errored, {metric.skipped} not executed[/bright_black]",
            )
        console.print(table)


@dataclass
class EvaluationEntry(Entity):
    """Evaluation entry."""

    run_id: str
    conversation: Conversation
    model_output: ModelOutput | None = None
    results: List[EvaluatorResult] = field(default_factory=list)
    status: TaskStatus = TaskStatus.RUNNING

    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs) -> "EvaluationEntry":
        data = dict(data)
        data["conversation"] = Conversation.from_dict(data["conversation"])
        output = data.get("output")
        data["model_output"] = ModelOutput.from_dict(output) if output else None

        run_id = data.get("evaluation_run_id") or data.get("execution_id")
        if run_id:
            data["run_id"] = run_id

        return super().from_dict(data, **kwargs)


class EvaluatorResult(BaseData):
    name: str
    status: TaskStatus = TaskStatus.RUNNING
    passed: bool | None = None
    error: str | None = None
    reason: str | None = None
