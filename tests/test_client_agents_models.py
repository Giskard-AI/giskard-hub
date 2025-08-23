import warnings
from unittest.mock import MagicMock, patch

import pytest

from giskard_hub.client import HubClient
from giskard_hub.resources.models import ModelsResource


@pytest.fixture
def mock_http_client():
    """Mock HTTP client for testing"""
    mock_client = MagicMock()

    # Mock successful OpenAPI response
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"openapi": "3.0.0"}
    mock_response.status_code = 200

    mock_client.get.return_value = mock_response
    return mock_client


@pytest.fixture
def hub_client(mock_http_client):
    """HubClient instance with mocked HTTP client"""
    with patch("httpx.Client", return_value=mock_http_client):
        client = HubClient(hub_url="http://test.example.com", api_key="test-api-key")
        return client


def test_agents_and_models_same_instance(hub_client):
    """Test that hub.agents and hub.models return the same instance"""
    assert hub_client.agents is hub_client.models
    assert isinstance(hub_client.agents, ModelsResource)
    assert isinstance(hub_client.models, ModelsResource)


def test_agents_and_models_same_methods(hub_client):
    """Test that both hub.agents and hub_client.models have the same methods"""
    agents_methods = set(dir(hub_client.agents))
    models_methods = set(dir(hub_client.models))

    # Core methods that should be available on both
    expected_methods = {"retrieve", "create", "update", "delete", "list", "chat"}

    for method in expected_methods:
        assert hasattr(
            hub_client.agents, method
        ), f"Method {method} missing from agents"
        assert hasattr(
            hub_client.models, method
        ), f"Method {method} missing from models"
        assert callable(
            getattr(hub_client.agents, method)
        ), f"Method {method} not callable on agents"
        assert callable(
            getattr(hub_client.models, method)
        ), f"Method {method} not callable on models"


def test_agents_and_models_same_behavior(hub_client):
    """Test that both properties behave identically for method calls"""
    # Mock the underlying _models resource
    mock_models = MagicMock(spec=ModelsResource)
    hub_client._models = mock_models

    # Test that calling methods on either property calls the same underlying resource
    hub_client.agents.list("project-123")
    mock_models.list.assert_called_once_with("project-123")

    # Reset mock
    mock_models.list.reset_mock()

    hub_client.models.list("project-123")
    mock_models.list.assert_called_once_with("project-123")


def test_models_deprecation_warning(hub_client):
    """Test that accessing hub.models shows a deprecation warning"""
    with pytest.warns(DeprecationWarning, match="The 'models' attribute is deprecated"):
        _ = hub_client.models


def test_agents_no_deprecation_warning(hub_client):
    """Test that accessing hub.agents does not show a deprecation warning"""
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        _ = hub_client.agents
        # Should not have any deprecation warnings
        deprecation_warnings = [
            warning for warning in w if issubclass(warning.category, DeprecationWarning)
        ]
        assert len(deprecation_warnings) == 0


def test_agents_preferred_over_models(hub_client):
    """Test that hub.agents is the preferred way to access the resource"""
    # Both should work identically
    agents_resource = hub_client.agents
    models_resource = hub_client.models

    assert agents_resource is models_resource

    # Test that we can call methods on both
    assert hasattr(agents_resource, "list")
    assert hasattr(models_resource, "list")

    # Test that they're the same object
    assert id(agents_resource) == id(models_resource)


def test_models_resource_methods_available(hub_client):
    """Test that all expected ModelsResource methods are available on both properties"""
    expected_methods = ["retrieve", "create", "update", "delete", "list", "chat"]

    for method_name in expected_methods:
        # Test on agents (preferred)
        assert hasattr(
            hub_client.agents, method_name
        ), f"Method {method_name} missing from agents"
        method = getattr(hub_client.agents, method_name)
        assert callable(method), f"Method {method_name} not callable on agents"

        # Test on models (deprecated)
        assert hasattr(
            hub_client.models, method_name
        ), f"Method {method_name} missing from models"
        method = getattr(hub_client.models, method_name)
        assert callable(method), f"Method {method_name} not callable on models"


def test_agents_models_resource_type(hub_client):
    """Test that both properties return the correct resource type"""
    from giskard_hub.resources.models import ModelsResource

    assert isinstance(hub_client.agents, ModelsResource)
    assert isinstance(hub_client.models, ModelsResource)

    # Test that they're the same instance
    assert hub_client.agents is hub_client.models


def test_agents_models_consistency_across_instances():
    """Test that the relationship between agents and models is consistent across different client instances"""
    with patch("httpx.Client") as mock_http_class:
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"openapi": "3.0.0"}
        mock_http_class.return_value = mock_client
        mock_client.get.return_value = mock_response

        # Create two different client instances
        client1 = HubClient(hub_url="http://test1.example.com", api_key="key1")
        client2 = HubClient(hub_url="http://test2.example.com", api_key="key2")

        # Each should have consistent behavior internally
        assert client1.agents is client1.models
        assert client2.agents is client2.models

        # But different instances should have different resources
        assert client1.agents is not client2.agents
        assert client1.models is not client2.models
