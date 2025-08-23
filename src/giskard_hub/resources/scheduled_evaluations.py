from __future__ import annotations

import warnings
from typing import List, Literal, Optional, Union

from ..data._base import NOT_GIVEN, NotGiven, filter_not_given
from ..data.evaluation import ScheduledEvaluationRun
from ..data.scheduled_evaluation import FrequencyOption, ScheduledEvaluation
from ..errors import HubValidationError
from ._resource import APIResource


class ScheduledEvaluationsResource(APIResource):
    """Resource for managing scheduled evaluations."""

    def _validate_schedule(
        self,
        *,
        frequency: Union[str, FrequencyOption, None] = None,
        day_of_week: Optional[int] = None,
        day_of_month: Optional[int] = None,
    ) -> None:
        """
        General validation for scheduled evaluation frequency and related fields.
        """
        if frequency is None:
            return

        # Normalize frequency to string for comparison
        freq = (
            str(frequency).lower()
            if isinstance(frequency, str)
            else getattr(frequency, "value", str(frequency)).lower()
        )

        if freq == "weekly":
            if day_of_week is None:
                raise HubValidationError(
                    "day_of_week must be provided when frequency is 'weekly'."
                )
        if freq == "monthly":
            if day_of_month is None:
                raise HubValidationError(
                    "day_of_month must be provided when frequency is 'monthly'."
                )
        if freq == "daily":
            if day_of_week is not None or day_of_month is not None:
                warnings.warn(
                    "day_of_week and day_of_month are ignored when frequency is 'daily'.",
                    UserWarning,
                )

    def _validate_schedule_update(
        self,
        frequency: Union[
            Literal["daily", "weekly", "monthly"], FrequencyOption, NotGiven
        ],
        day_of_week: Union[int, NotGiven],
        day_of_month: Union[int, NotGiven],
    ) -> None:
        """Validate schedule fields when updating a scheduled evaluation."""
        # Only validate if any schedule-related fields are being updated
        freq_val: Optional[
            Union[Literal["daily", "weekly", "monthly"], FrequencyOption]
        ] = None
        dow_val: Optional[int] = None
        dom_val: Optional[int] = None

        if frequency is not NOT_GIVEN:
            freq_val = frequency  # type: ignore
        if day_of_week is not NOT_GIVEN:
            dow_val = day_of_week  # type: ignore
        if day_of_month is not NOT_GIVEN:
            dom_val = day_of_month  # type: ignore

        if freq_val is not None or dow_val is not None or dom_val is not None:
            self._validate_schedule(
                frequency=freq_val,
                day_of_week=dow_val,
                day_of_month=dom_val,
            )

    def list(
        self,
        *,
        project_id: str,
    ) -> List[ScheduledEvaluation]:
        """List scheduled evaluations for a project.

        Parameters
        ----------
        project_id : str
            The ID of the project to list scheduled evaluations for.

        Returns
        -------
        List[ScheduledEvaluation]
            List of scheduled evaluations.
        """
        return self._client.get(
            "/scheduled-evaluations",
            params={"project_id": project_id},
            cast_to=ScheduledEvaluation,
        )

    def retrieve(self, scheduled_evaluation_id: str) -> ScheduledEvaluation:
        """Retrieve a scheduled evaluation by ID.

        Parameters
        ----------
        scheduled_evaluation_id : str
            The ID of the scheduled evaluation to retrieve.

        Returns
        -------
        ScheduledEvaluation
            The scheduled evaluation.
        """
        return self._client.get(
            f"/scheduled-evaluations/{scheduled_evaluation_id}",
            cast_to=ScheduledEvaluation,
        )

    def create(  # pylint: disable=too-many-arguments
        self,
        *,
        project_id: str,
        name: str,
        model_id: str,
        dataset_id: str,
        frequency: Union[Literal["daily", "weekly", "monthly"], FrequencyOption],
        time: str,
        tags: Optional[List[str]] = None,
        run_count: int = 1,
        day_of_week: Optional[int] = None,
        day_of_month: Optional[int] = None,
    ) -> ScheduledEvaluation:
        """Create a new scheduled evaluation.

        Parameters
        ----------
        project_id : str
            The ID of the project to create the scheduled evaluation in.
        name : str
            The name of the scheduled evaluation.
        model_id : str
            The ID of the model to evaluate.
        dataset_id : str
            The ID of the dataset to evaluate against.
        frequency : str
            The frequency of the scheduled evaluation (daily, weekly, monthly).
        time : str
            The time to run the evaluation (HH:MM format).
        tags : List[str], optional
            List of tags to filter the conversations that will be evaluated.
        run_count : int, optional
            The number of times to run each test case (1-5), by default 1.
        day_of_week : int, optional
            The day of the week to run (1-7, 1 is Monday). Required for weekly frequency.
        day_of_month : int, optional
            The day of the month to run (1-28). Required for monthly frequency.

        Returns
        -------
        ScheduledEvaluation
            The created scheduled evaluation.
        """
        self._validate_schedule(
            frequency=frequency,
            day_of_week=day_of_week,
            day_of_month=day_of_month,
        )

        payload = {
            "project_id": project_id,
            "name": name,
            "model_id": model_id,
            "dataset_id": dataset_id,
            "frequency": frequency,
            "time": time,
            "run_count": run_count,
        }
        if tags is not None:
            payload["tags"] = tags
        if day_of_week is not None:
            payload["day_of_week"] = day_of_week
        if day_of_month is not None:
            payload["day_of_month"] = day_of_month

        return self._client.post(
            "/scheduled-evaluations",
            json=payload,
            cast_to=ScheduledEvaluation,
        )

    def update(  # pylint: disable=too-many-arguments
        self,
        scheduled_evaluation_id: str,
        *,
        name: Union[str, NotGiven] = NOT_GIVEN,
        model_id: Union[str, NotGiven] = NOT_GIVEN,
        dataset_id: Union[str, NotGiven] = NOT_GIVEN,
        frequency: Union[
            Literal["daily", "weekly", "monthly"], FrequencyOption, NotGiven
        ] = NOT_GIVEN,
        time: Union[str, NotGiven] = NOT_GIVEN,
        tags: Union[List[str], NotGiven] = NOT_GIVEN,
        run_count: Union[int, NotGiven] = NOT_GIVEN,
        day_of_week: Union[int, NotGiven] = NOT_GIVEN,
        day_of_month: Union[int, NotGiven] = NOT_GIVEN,
        paused: Union[bool, NotGiven] = NOT_GIVEN,
    ) -> ScheduledEvaluation:
        """Update a scheduled evaluation.

        Parameters
        ----------
        scheduled_evaluation_id : str
            The ID of the scheduled evaluation to update.
        name : str, optional
            The name of the scheduled evaluation.
        model_id : str, optional
            The ID of the model to evaluate.
        dataset_id : str, optional
            The ID of the dataset to evaluate against.
        frequency : str, optional
            The frequency of the scheduled evaluation (daily, weekly, monthly).
        time : str, optional
            The time to run the evaluation (HH:MM format).
        tags : List[str], optional
            List of tags to filter the conversations that will be evaluated.
        run_count : int, optional
            The number of times to run each test case (1-5).
        day_of_week : int, optional
            The day of the week to run (1-7, 1 is Monday). Required for weekly frequency.
        day_of_month : int, optional
            The day of the month to run (1-28). Required for monthly frequency.
        paused : bool, optional
            Whether the scheduled evaluation is paused.

        Returns
        -------
        ScheduledEvaluation
            The updated scheduled evaluation.
        """
        # Validate schedule if any schedule-related fields are being updated
        self._validate_schedule_update(frequency, day_of_week, day_of_month)

        payload = filter_not_given(
            {
                "name": name,
                "model_id": model_id,
                "dataset_id": dataset_id,
                "frequency": frequency,
                "time": time,
                "tags": tags,
                "run_count": run_count,
                "day_of_week": day_of_week,
                "day_of_month": day_of_month,
                "paused": paused,
            }
        )

        return self._client.patch(
            f"/scheduled-evaluations/{scheduled_evaluation_id}",
            json=payload,
            cast_to=ScheduledEvaluation,
        )

    def delete(self, scheduled_evaluation_ids: Union[str, List[str]]) -> None:
        """Delete scheduled evaluations.

        Parameters
        ----------
        scheduled_evaluation_ids : Union[str, List[str]]
            List of scheduled evaluation IDs or a single scheduled evaluation ID to delete.
        """
        self._client.delete(
            "/scheduled-evaluations",
            params={"scheduled_evaluation_ids": scheduled_evaluation_ids},
        )

    def list_evaluations(
        self, scheduled_evaluation_id: str
    ) -> List[ScheduledEvaluationRun]:
        """List evaluations linked to a scheduled evaluation.

        Parameters
        ----------
        scheduled_evaluation_id : str
            The ID of the scheduled evaluation to get evaluations for.

        Returns
        -------
        List[ScheduledEvaluationRun]
            List of evaluations linked to the scheduled evaluation.
        """
        return self._client.get(
            f"/scheduled-evaluations/{scheduled_evaluation_id}/evaluations",
            cast_to=ScheduledEvaluationRun,
        )
