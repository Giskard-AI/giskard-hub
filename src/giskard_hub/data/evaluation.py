from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List

from rich.console import Console
from rich.table import Table

from ._base import BaseData
from ._entity import Entity, EntityWithTaskProgress
from .chat_test_case import ChatTestCase
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


@dataclass(kw_only=True)
# pylint: disable=too-many-instance-attributes
class EvaluationRun(EntityWithTaskProgress):
    """Evaluation run."""

    name: str | None = None
    project_id: str | None = None
    datasets: List[Dataset] = field(default_factory=list)
    model: Model | None = None
    criteria: List = field(default_factory=list)
    metrics: List[Metric] = field(default_factory=list)
    tags: List[Metric] = field(default_factory=list)
    failure_categories: Dict[str, int] = field(default_factory=dict)
    progress: TaskProgress | None = None

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
class ScheduledEvaluationRun(EvaluationRun):
    """Evaluation run linked to a scheduled evaluation.

    This extends EvaluationRun to include additional fields specific to
    scheduled evaluation runs, such as scheduled_evaluation_id.
    """

    scheduled_evaluation_id: str | None = None
    target_datasets: List[Dict[str, Any]] = field(default_factory=list)
    failure_categories: Dict[str, int] = field(default_factory=dict)
    local: bool = False

    # Tags field for scheduled evaluation runs (different structure than parent class)
    scheduled_tags: List[Dict[str, Any]] = field(default_factory=list)

    # Datasets field for scheduled evaluation runs (different structure than parent class)
    scheduled_datasets: List[Dict[str, Any]] = field(default_factory=list)

    # Metrics field for scheduled evaluation runs (different structure than parent class)
    scheduled_metrics: List[Dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs) -> "ScheduledEvaluationRun":
        # Extract fields specific to scheduled evaluation runs
        scheduled_evaluation_id = data.get("scheduled_evaluation_id")
        target_datasets = data.get("target_datasets", [])
        failure_categories = data.get("failure_categories", {})
        local = data.get("local", False)
        scheduled_tags_data = data.get("tags", [])
        scheduled_datasets_data = data.get("datasets", [])
        scheduled_metrics_data = data.get("metrics", [])

        # Handle the status field mapping to progress for parent class
        if "status" in data and "progress" not in data:
            data["progress"] = data["status"]

        # Remove fields from data to prevent parent class from processing them
        data_for_parent = data.copy()
        if "tags" in data_for_parent:
            del data_for_parent["tags"]
        if "datasets" in data_for_parent:
            del data_for_parent["datasets"]
        if "metrics" in data_for_parent:
            del data_for_parent["metrics"]

        # Call parent class method and cast to correct type
        instance = super().from_dict(data_for_parent, **kwargs)
        if isinstance(instance, EvaluationRun):
            # Create new instance with additional fields
            new_data = instance.__dict__.copy()
            new_data["scheduled_evaluation_id"] = scheduled_evaluation_id
            new_data["target_datasets"] = target_datasets
            new_data["failure_categories"] = failure_categories
            new_data["local"] = local
            new_data["scheduled_tags"] = scheduled_tags_data
            new_data["scheduled_datasets"] = scheduled_datasets_data
            new_data["scheduled_metrics"] = scheduled_metrics_data
            return cls(**new_data)

        return instance


@dataclass
class EvaluationEntry(Entity):
    """Evaluation entry."""

    run_id: str
    conversation: Conversation | ChatTestCase
    model_output: ModelOutput | None = None
    results: List[EvaluatorResult] = field(default_factory=list)
    status: TaskStatus = TaskStatus.RUNNING

    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs) -> "EvaluationEntry":
        data = dict(data)

        if "chat_test_case" in data:
            data["conversation"] = ChatTestCase.from_dict(data["chat_test_case"])
        else:
            data["conversation"] = Conversation.from_dict(data["conversation"])

        output = data.get("output")
        data["model_output"] = ModelOutput.from_dict(output) if output else None

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
