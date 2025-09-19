from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List

from rich.console import Console
from rich.table import Table

from ._base import BaseData
from ._entity import Entity, EntityWithTaskProgress
from .chat_test_case import ChatTestCase
from .dataset import Dataset
from .model import Model, ModelOutput
from .project import FailureCategory
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
# pylint: disable=too-many-instance-attributes
class EvaluationRun(EntityWithTaskProgress):
    """Evaluation run."""

    name: str | None
    project_id: str | None
    datasets: List[Dataset] = field(default_factory=list)
    model: Model | None = None
    criteria: List = field(default_factory=list)
    metrics: List[Metric] = field(default_factory=list)
    tags: List[Metric] = field(default_factory=list)
    failure_categories: Dict[str, int] = field(default_factory=dict)
    scheduled_evaluation_id: str | None = None

    @property
    def resource(self) -> str:
        return "evaluations"

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
            if math.isnan(metric.percentage):
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
class FailureCategoryResult(BaseData):
    category: FailureCategory | None
    status: TaskStatus | None
    error: str | None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FailureCategoryResult":
        data = dict(data)

        category = data.get("category")
        data["category"] = FailureCategory.from_dict(category) if category else None

        status = data.get("status")
        data["status"] = TaskStatus(status) if status else None

        return super().from_dict(data)


@dataclass
class EvaluationEntry(Entity):
    """Evaluation entry."""

    run_id: str
    chat_test_case: ChatTestCase
    model_output: ModelOutput | None = None
    results: List[EvaluatorResult] = field(default_factory=list)
    status: TaskStatus = TaskStatus.RUNNING
    failure_category: FailureCategoryResult | None = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs) -> "EvaluationEntry":
        data = dict(data)

        # Process `chat_test_case` payload
        data["chat_test_case"] = ChatTestCase.from_dict(data["chat_test_case"])

        output = data.get("output")
        data["model_output"] = ModelOutput.from_dict(output) if output else None

        failure_category = data.get("failure_category")
        data["failure_category"] = (
            FailureCategoryResult.from_dict(failure_category)
            if failure_category
            else None
        )

        run_id = data.get("evaluation_id")
        if run_id:
            data["run_id"] = run_id

        return super().from_dict(data, **kwargs)


class EvaluatorResult(BaseData):
    name: str
    status: TaskStatus = TaskStatus.RUNNING
    passed: bool | None = None
    error: str | None = None
    reason: str | None = None
