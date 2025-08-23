from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Literal, Union

from dateutil import parser

from ._entity import Entity, EntityWithTaskProgress


class FrequencyOption(str, Enum):
    """Frequency options for scheduled evaluations."""

    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


@dataclass
class SuccessExecutionStatus:
    """Success execution status for scheduled evaluations."""

    evaluation_id: str
    status: Literal["success"] = "success"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SuccessExecutionStatus":
        return cls(**data)


@dataclass
class ErrorExecutionStatus:
    """Error execution status for scheduled evaluations."""

    error_message: str
    status: Literal["error"] = "error"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ErrorExecutionStatus":
        return cls(**data)


ExecutionStatus = Union[SuccessExecutionStatus, ErrorExecutionStatus]


@dataclass(kw_only=True)
class ScheduledEvaluation(
    EntityWithTaskProgress
):  # pylint: disable=too-many-instance-attributes
    """Scheduled evaluation entity.

    Attributes
    ----------
    project_id : str
        The ID of the project this scheduled evaluation belongs to.
    name : str
        The name of the scheduled evaluation.
    model_id : str
        The ID of the model to evaluate.
    dataset_id : str
        The ID of the dataset to evaluate against.
    tags : List[str], optional
        List of tags to filter the conversations that will be evaluated.
    run_count : int
        The number of times to run each test case (1-5).
    frequency : FrequencyOption
        The frequency of the scheduled evaluation (daily, weekly, monthly).
    time : str
        The time to run the evaluation (HH:MM format).
    day_of_week : int, optional
        The day of the week to run (1-7, 1 is Monday). Required for weekly frequency.
    day_of_month : int, optional
        The day of the month to run (1-28). Required for monthly frequency.
    last_execution_at : datetime, optional
        The timestamp of the last execution.
    last_execution_status : ExecutionStatus, optional
        The status of the last execution.
    paused : bool
        Whether the scheduled evaluation is paused.
    """

    project_id: str
    name: str
    model_id: str
    dataset_id: str
    tags: list[str] = field(default_factory=list)
    run_count: int = 1
    frequency: FrequencyOption = FrequencyOption.DAILY
    time: str = "00:00"
    day_of_week: int | None = None
    day_of_month: int | None = None
    paused: bool = False
    last_execution_at: datetime | None = None
    last_execution_status: ExecutionStatus | None = None

    @classmethod
    def from_dict(
        cls, data: dict[str, Any], *, _client=None, **kwargs: Any
    ) -> "Entity":
        data = dict(data)
        if data.get("frequency"):
            data["frequency"] = FrequencyOption(data["frequency"])
        if data.get("last_run"):
            data["last_run"] = parser.parse(data["last_run"])
        if data.get("next_run"):
            data["next_run"] = parser.parse(data["next_run"])
        if data.get("last_execution_at"):
            data["last_execution_at"] = parser.parse(data["last_execution_at"])

        # Handle execution status
        if data.get("last_execution_status"):
            status_data = data["last_execution_status"]
            if status_data.get("status") == "success":
                data["last_execution_status"] = SuccessExecutionStatus.from_dict(
                    status_data
                )
            elif status_data.get("status") == "error":
                data["last_execution_status"] = ErrorExecutionStatus.from_dict(
                    status_data
                )

        return super().from_dict(data, _client=_client, **kwargs)

    @property
    def resource(self) -> str:
        return "scheduled_evaluations"
