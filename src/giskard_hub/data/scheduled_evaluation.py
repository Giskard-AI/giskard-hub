from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Union

from ._base import BaseData
from ._entity import Entity


class FrequencyOption(str, Enum):
    """Frequency options for scheduled evaluations."""

    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


@dataclass
class SuccessExecutionStatus(BaseData):
    """Success execution status for scheduled evaluations."""

    evaluation_id: str
    status: Literal["success"] = "success"


@dataclass
class ErrorExecutionStatus(BaseData):
    """Error execution status for scheduled evaluations."""

    error_message: str
    status: Literal["error"] = "error"


ExecutionStatus = Union[SuccessExecutionStatus, ErrorExecutionStatus]


@dataclass
class ScheduledEvaluation(Entity):
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
    tags: List[str] = field(default_factory=list)
    run_count: int = 1
    frequency: FrequencyOption = FrequencyOption.DAILY
    time: str = "00:00"
    day_of_week: Optional[int] = None
    day_of_month: Optional[int] = None
    last_execution_at: Optional[datetime] = None
    last_execution_status: Optional[ExecutionStatus] = None
    paused: bool = False

    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs) -> ScheduledEvaluation:
        data = dict(data)

        # Handle execution status
        last_execution_status = data.get("last_execution_status")
        if last_execution_status:
            if last_execution_status.get("status") == "success":
                data["last_execution_status"] = SuccessExecutionStatus.from_dict(
                    last_execution_status
                )
            elif last_execution_status.get("status") == "error":
                data["last_execution_status"] = ErrorExecutionStatus.from_dict(
                    last_execution_status
                )

        # Handle datetime
        last_execution_at = data.get("last_execution_at")
        if last_execution_at:
            data["last_execution_at"] = datetime.fromisoformat(
                last_execution_at.replace("Z", "+00:00")
            )

        result = super().from_dict(data, **kwargs)
        return result

    def refresh(self) -> ScheduledEvaluation:
        """Refresh the scheduled evaluation from the Hub."""
        if not self._client or not self.id:
            raise ValueError(
                "This scheduled evaluation instance is detached or unsaved and cannot be refreshed."
            )

        data = self._client.scheduled_evaluations.retrieve(self.id)
        self._hydrate(data)

        return self
