from giskard_hub.data.knowledge_base import KnowledgeBase
from giskard_hub.data.task import TaskStatus


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
        assert kb.progress is not None
        assert kb.progress.status == TaskStatus.FINISHED
        assert kb.progress.current == 100
        assert kb.progress.total == 100

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
        assert kb.progress is None
