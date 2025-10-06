import uuid

from giskard_hub.data.scan import ProbeAttempt, ReviewStatus


class TestProbeAttempt:
    """Test the ProbeAttempt data model."""

    def test_probe_attempt_from_dict_full(self):
        attempt_id = str(uuid.uuid4())
        probe_result_id = str(uuid.uuid4())
        data = {
            "id": attempt_id,
            "probe_result_id": probe_result_id,
            "messages": [
                {
                    "role": "user",
                    "content": "What is the issue?",
                    "metadata": {"timestamp": "2025-10-06T12:00:00Z"},
                },
                {
                    "role": "assistant",
                    "content": "The model is biased.",
                    "metadata": {"timestamp": "2025-10-06T12:05:00Z"},
                },
            ],
            "metadata": {"attempt_number": 1},
            "severity": 20,
            "review_status": ReviewStatus.ACKNOWLEDGED.value,
            "reason": "Detected bias in predictions",
            "error": {
                "message": "No error",
            },
        }
        attempt = ProbeAttempt.from_dict(data)
        assert attempt.id == attempt_id
        assert attempt.probe_result_id == probe_result_id
        assert len(attempt.messages) == 2
        assert attempt.messages[0].role == "user"
        assert attempt.messages[0].content == "What is the issue?"
        assert attempt.messages[0].metadata["timestamp"] == "2025-10-06T12:00:00Z"
        assert attempt.messages[1].role == "assistant"
        assert attempt.messages[1].content == "The model is biased."
        assert attempt.messages[1].metadata["timestamp"] == "2025-10-06T12:05:00Z"
        assert attempt.metadata["attempt_number"] == 1
        assert attempt.severity == 20
        assert attempt.review_status == ReviewStatus.ACKNOWLEDGED
        assert attempt.reason == "Detected bias in predictions"
        assert attempt.error is not None
        assert attempt.error.message == "No error"

    def test_probe_attempt_from_dict_minimal(self):
        attempt_id = str(uuid.uuid4())
        probe_result_id = str(uuid.uuid4())
        data = {
            "id": attempt_id,
            "probe_result_id": probe_result_id,
            "messages": [],
            "metadata": {},
            "severity": 0,
            "review_status": ReviewStatus.PENDING.value,
            "reason": "Initial attempt",
        }
        attempt = ProbeAttempt.from_dict(data)
        assert attempt.id == attempt_id
        assert attempt.probe_result_id == probe_result_id
        assert attempt.messages == []
        assert attempt.metadata == {}
        assert attempt.severity == 0
        assert attempt.review_status == ReviewStatus.PENDING
        assert attempt.reason == "Initial attempt"
        assert attempt.error is None
