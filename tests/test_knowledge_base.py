from unittest.mock import MagicMock, patch

import pytest

from giskard_hub.data.knowledge_base import KnowledgeBase, Topic
from giskard_hub.data.task import TaskProgress, TaskStatus


class TestKnowledgeBase:
    """Test the KnowledgeBase class."""

    def test_from_dict_with_status(self):
        """Test from_dict when status is provided."""
        data = {
            "name": "Test KB",
            "project_id": "project-1",
            "description": "Test description",
            "n_documents": 5,
            "topics": [],
            "status": {
                "state": "finished",
                "current": 100,
                "total": 100,
                "error": None,
            },
        }

        kb = KnowledgeBase.from_dict(data)
        assert kb.name == "Test KB"
        assert kb.project_id == "project-1"
        assert kb.status is not None
        assert kb.status.status == TaskStatus.FINISHED
        assert kb.status.current == 100
        assert kb.status.total == 100

    def test_from_dict_without_status(self):
        """Test from_dict when no status is provided."""
        data = {
            "name": "Test KB",
            "project_id": "project-1",
            "description": "Test description",
            "n_documents": 5,
            "topics": [],
        }

        kb = KnowledgeBase.from_dict(data)
        assert kb.name == "Test KB"
        assert kb.status is None

    def test_is_processing_with_status_running(self):
        """Test is_processing when status is running."""
        status = TaskProgress(status=TaskStatus.RUNNING, current=50, total=100)
        kb = KnowledgeBase(
            name="Test KB",
            project_id="project-1",
            description="Test description",
            status=status,
            topics=[],
        )
        assert kb.is_processing()

    def test_is_processing_with_status_finished(self):
        """Test is_processing when status is finished."""
        status = TaskProgress(status=TaskStatus.FINISHED, current=100, total=100)
        kb = KnowledgeBase(
            name="Test KB",
            project_id="project-1",
            description="Test description",
            status=status,
            topics=[],
        )
        assert not kb.is_processing()

    def test_is_processing_fallback(self):
        """Test is_processing fallback when no status."""
        kb = KnowledgeBase(
            name="Test KB",
            project_id="project-1",
            description="Test description",
            topics=[],
        )
        assert kb.is_processing()

    def test_is_ready_with_status_finished(self):
        """Test is_ready when status is finished."""
        status = TaskProgress(status=TaskStatus.FINISHED, current=100, total=100)
        kb = KnowledgeBase(
            name="Test KB",
            project_id="project-1",
            description="Test description",
            status=status,
            topics=[],
        )
        assert kb.is_ready()

    def test_is_ready_with_status_running(self):
        """Test is_ready when status is running."""
        status = TaskProgress(status=TaskStatus.RUNNING, current=50, total=100)
        kb = KnowledgeBase(
            name="Test KB",
            project_id="project-1",
            description="Test description",
            status=status,
            topics=[],
        )
        assert not kb.is_ready()

    def test_is_ready_fallback(self):
        """Test is_ready fallback when no status."""
        topics = [Topic(name="Topic 1", description="First topic")]
        kb = KnowledgeBase(
            name="Test KB",
            project_id="project-1",
            description="Test description",
            topics=topics,
        )
        assert kb.is_ready()

    def test_is_errored_with_status_error(self):
        """Test is_errored when status is error."""
        status = TaskProgress(
            status=TaskStatus.ERROR, current=0, total=100, error="Processing failed"
        )
        kb = KnowledgeBase(
            name="Test KB",
            project_id="project-1",
            description="Test description",
            status=status,
            topics=[],
        )
        assert kb.is_errored()

    def test_is_errored_with_status_finished(self):
        """Test is_errored when status is finished."""
        status = TaskProgress(status=TaskStatus.FINISHED, current=100, total=100)
        kb = KnowledgeBase(
            name="Test KB",
            project_id="project-1",
            description="Test description",
            status=status,
            topics=[],
        )
        assert not kb.is_errored()

    def test_is_errored_fallback(self):
        """Test is_errored fallback when no status."""
        kb = KnowledgeBase(
            name="Test KB",
            project_id="project-1",
            description="Test description",
            n_documents=0,
            topics=[],
        )
        assert kb.is_errored()

    def test_refresh_success(self):
        """Test successful refresh of knowledge base."""
        mock_client = MagicMock()
        mock_topics = [Topic(name="Topic 1", description="First topic")]
        mock_status = TaskProgress(status=TaskStatus.FINISHED, current=100, total=100)

        # Mock the retrieve response
        mock_kb_data = KnowledgeBase(
            name="Updated KB",
            project_id="project-1",
            description="Updated description",
            topics=mock_topics,
            n_documents=10,
            status=mock_status,
        )
        mock_kb_data._client = mock_client
        mock_kb_data.id = "kb-1"

        mock_client.knowledge_bases.retrieve.return_value = mock_kb_data

        # Create KB instance with client
        kb = KnowledgeBase(
            name="Test KB",
            project_id="project-1",
            description="Test description",
            topics=[],
        )
        kb._client = mock_client
        kb.id = "kb-1"

        # Test refresh
        result = kb.refresh()

        mock_client.knowledge_bases.retrieve.assert_called_once_with("kb-1")
        assert result.topics == mock_topics
        assert result.n_documents == 10
        assert result.status == mock_status

    def test_refresh_no_client(self):
        """Test refresh fails when no client is attached."""
        kb = KnowledgeBase(
            name="Test KB", project_id="project-1", description="Test description"
        )
        # No _client set

        with pytest.raises(ValueError, match="detached or unsaved"):
            kb.refresh()

    def test_refresh_no_id(self):
        """Test refresh fails when no ID is set."""
        mock_client = MagicMock()
        kb = KnowledgeBase(
            name="Test KB", project_id="project-1", description="Test description"
        )
        kb._client = mock_client
        # No id set

        with pytest.raises(ValueError, match="detached or unsaved"):
            kb.refresh()

    @patch("time.sleep")
    def test_wait_for_completion_success_with_status(self, mock_sleep):
        """Test successful wait_for_completion with status tracking."""
        mock_client = MagicMock()

        # Create KB with running status initially
        status = TaskProgress(status=TaskStatus.RUNNING, current=50, total=100)
        kb = KnowledgeBase(
            name="Test KB",
            project_id="project-1",
            description="Test description",
            status=status,
            topics=[],
        )
        kb._client = mock_client
        kb.id = "kb-1"

        # Mock the refresh method to simulate status progression
        def mock_refresh():
            if kb.status.status == TaskStatus.RUNNING:
                kb.status = TaskProgress(
                    status=TaskStatus.FINISHED, current=100, total=100
                )
            return kb

        kb.refresh = mock_refresh

        # Test wait_for_completion
        result = kb.wait_for_completion(timeout=30, poll_interval=1)

        assert kb.is_ready()
        assert result.status.status == TaskStatus.FINISHED

    @patch("time.sleep")
    def test_wait_for_completion_success_fallback(self, mock_sleep):
        """Test successful wait_for_completion with fallback behavior."""
        mock_client = MagicMock()

        # Create KB with no status (fallback mode)
        kb = KnowledgeBase(
            name="Test KB",
            project_id="project-1",
            description="Test description",
            topics=[],
        )
        kb._client = mock_client
        kb.id = "kb-1"

        # Mock the refresh method to simulate topics being populated
        def mock_refresh():
            if len(kb.topics) == 0:
                kb.topics = [Topic(name="Topic 1", description="First topic")]
            return kb

        kb.refresh = mock_refresh

        # Test wait_for_completion
        result = kb.wait_for_completion(timeout=30, poll_interval=1)

        assert kb.is_ready()
        assert len(result.topics) == 1
        assert result.topics[0].name == "Topic 1"

    @patch("time.sleep")
    def test_wait_for_completion_timeout(self, mock_sleep):
        """Test wait_for_completion times out."""
        mock_client = MagicMock()

        # Create KB with running status
        status = TaskProgress(status=TaskStatus.RUNNING, current=50, total=100)
        kb = KnowledgeBase(
            name="Test KB",
            project_id="project-1",
            description="Test description",
            status=status,
            topics=[],
        )
        kb._client = mock_client
        kb.id = "kb-1"

        # Mock refresh to always return running status
        def mock_refresh():
            kb.status = TaskProgress(status=TaskStatus.RUNNING, current=50, total=100)
            return kb

        kb.refresh = mock_refresh

        # Test wait_for_completion with short timeout
        with pytest.raises(TimeoutError, match="did not finish in time"):
            kb.wait_for_completion(timeout=0.1, poll_interval=0.05)

    @patch("time.sleep")
    def test_wait_for_completion_immediate_success(self, mock_sleep):
        """Test wait_for_completion when already finished."""
        mock_client = MagicMock()

        # Create KB with finished status
        status = TaskProgress(status=TaskStatus.FINISHED, current=100, total=100)
        kb = KnowledgeBase(
            name="Test KB",
            project_id="project-1",
            description="Test description",
            status=status,
            topics=[],
        )
        kb._client = mock_client
        kb.id = "kb-1"

        # Mock refresh to not change status
        def mock_refresh():
            return kb

        kb.refresh = mock_refresh

        # Test wait_for_completion
        result = kb.wait_for_completion(timeout=30, poll_interval=1)

        assert kb.is_ready()
        # Should not have called sleep since already finished
        mock_sleep.assert_not_called()

    @patch("time.sleep")
    def test_wait_for_completion_errored_with_status(self, mock_sleep):
        """Test wait_for_completion when status shows error."""
        mock_client = MagicMock()

        # Create KB with error status
        status = TaskProgress(
            status=TaskStatus.ERROR,
            current=0,
            total=100,
            error="Processing failed due to invalid format",
        )
        kb = KnowledgeBase(
            name="Test KB",
            project_id="project-1",
            description="Test description",
            status=status,
            topics=[],
        )
        kb._client = mock_client
        kb.id = "kb-1"

        # Mock refresh to keep error status
        def mock_refresh():
            return kb

        kb.refresh = mock_refresh

        # Test wait_for_completion
        with pytest.raises(
            RuntimeError, match="Processing failed due to invalid format"
        ):
            kb.wait_for_completion(timeout=0.1, poll_interval=0.05)

    @patch("time.sleep")
    def test_wait_for_completion_errored_fallback(self, mock_sleep):
        """Test wait_for_completion when fallback error detection triggers."""
        mock_client = MagicMock()

        # Create KB with no status (fallback mode)
        kb = KnowledgeBase(
            name="Test KB",
            project_id="project-1",
            description="Test description",
            n_documents=0,
            topics=[],
        )
        kb._client = mock_client
        kb.id = "kb-1"

        # Mock refresh to simulate error state
        def mock_refresh():
            # Keep the error state
            kb.n_documents = 0
            kb.topics = []
            return kb

        kb.refresh = mock_refresh

        # Test wait_for_completion
        with pytest.raises(RuntimeError, match="processing failed"):
            kb.wait_for_completion(timeout=0.1, poll_interval=0.05)

    @patch("time.sleep")
    def test_wait_for_completion_aborted(self, mock_sleep):
        """Test wait_for_completion when processing is aborted."""
        mock_client = MagicMock()

        # Create KB with no topics
        kb = KnowledgeBase(
            name="Test KB",
            project_id="project-1",
            description="Test description",
            topics=[],
        )
        kb._client = mock_client
        kb.id = "kb-1"

        # Mock refresh to simulate processing being aborted (not processing but not ready)
        def mock_refresh():
            # Simulate a state where processing was aborted
            kb.topics = []  # Keep empty but mark as not processing
            return kb

        kb.refresh = mock_refresh

        # Override is_processing to simulate aborted state
        kb.is_processing = lambda: False
        kb.is_ready = lambda: False

        # Test wait_for_completion
        with pytest.raises(RuntimeError, match="was aborted"):
            kb.wait_for_completion(timeout=0.1, poll_interval=0.05)
