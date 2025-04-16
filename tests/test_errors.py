import json
from unittest.mock import Mock

import httpx
import pytest

from giskard_hub._base_client import SyncClient
from giskard_hub.errors import (
    HubAPIError,
    HubAuthenticationError,
    HubConnectionError,
    HubForbiddenError,
    HubJSONDecodeError,
    HubValidationError,
)


class MockSyncClient(SyncClient):
    """Test client that allows mocking responses"""

    def __init__(self):
        self._http = Mock()


def test_hub_connection_error():
    """Test handling of hub connection errors"""

    client = MockSyncClient()
    response = Mock()
    response.raise_for_status.return_value = None
    response.json.return_value = {}
    client._http.get.return_value = response

    # Test with no openapi field in response
    with pytest.raises(HubConnectionError) as exc_info:
        resp = client._http.get("/openapi.json")
        resp.raise_for_status()
        data = resp.json()
        if "openapi" not in data:
            raise HubConnectionError(
                "The response doesn't appear to include an OpenAPI specification"
            )

    assert isinstance(exc_info.value, HubConnectionError)
    assert (
        exc_info.value.message
        == "The response doesn't appear to include an OpenAPI specification"
    )

    # Test with connection error
    client._http.get.side_effect = Exception("Connection failed")
    with pytest.raises(HubConnectionError) as exc_info:
        try:
            resp = client._http.get("/openapi.json")
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            raise HubConnectionError("Failed to connect to Giskard Hub") from e

    assert isinstance(exc_info.value, HubConnectionError)
    assert exc_info.value.message == "Failed to connect to Giskard Hub"


def test_authentication_error():
    """Test handling of 401 authentication errors"""
    client = MockSyncClient()
    response = Mock()
    response.status_code = 401
    response.text = "Unauthorized"
    client._http.request.return_value = response

    with pytest.raises(HubAuthenticationError) as exc_info:
        client.get("/test")

    assert isinstance(exc_info.value, HubAuthenticationError)
    assert exc_info.value.status_code == 401
    assert exc_info.value.message == "Authentication failed: please check your API key"
    assert exc_info.value.response_text == "Unauthorized"


def test_forbidden_error():
    """Test handling of 403 forbidden errors"""
    client = MockSyncClient()
    response = Mock()
    response.status_code = 403
    response.text = "Forbidden"
    response.json.return_value = {"message": "Access denied"}
    client._http.request.return_value = response

    with pytest.raises(HubForbiddenError) as exc_info:
        client.get("/test")

    assert isinstance(exc_info.value, HubForbiddenError)
    assert exc_info.value.status_code == 403
    assert exc_info.value.message == "Access denied"
    assert exc_info.value.response_text == "Forbidden"


def test_validation_error():
    """Test handling of 422 validation errors"""
    client = MockSyncClient()
    response = Mock()
    response.status_code = 422
    response.text = "Invalid request"
    response.json.return_value = {
        "message": "Invalid input",
        "fields": {"name": "Name is required"},
    }
    client._http.request.return_value = response

    with pytest.raises(HubValidationError) as exc_info:
        client.get("/test")

    assert isinstance(exc_info.value, HubValidationError)
    assert exc_info.value.status_code == 422
    assert "Invalid input" in exc_info.value.message
    assert "Name is required" in exc_info.value.message
    assert exc_info.value.response_text == "Invalid request"


def test_json_decode_error():
    """Test handling of invalid JSON responses"""
    client = MockSyncClient()
    response = Mock()
    response.status_code = 200
    response.text = "Invalid JSON"
    response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
    client._http.request.return_value = response

    with pytest.raises(HubJSONDecodeError) as exc_info:
        client.get("/test")

    assert isinstance(exc_info.value, HubJSONDecodeError)
    assert exc_info.value.status_code == 200
    assert "Failed to decode API response as JSON" in exc_info.value.message
    assert exc_info.value.response_text == "Invalid JSON"


def test_general_api_error():
    """Test handling of general API errors"""
    client = MockSyncClient()
    response = Mock()
    response.status_code = 500
    response.text = "Server error"
    response.json.return_value = {"message": "Internal server error"}
    client._http.request.return_value = response

    # Mock raise_for_status to raise an HTTPStatusError
    http_error = httpx.HTTPStatusError(
        "Server error", request=Mock(), response=response
    )
    response.raise_for_status.side_effect = http_error

    with pytest.raises(HubAPIError) as exc_info:
        client.get("/test")

    assert isinstance(exc_info.value, HubAPIError)
    assert exc_info.value.status_code == 500
    assert exc_info.value.message == "Internal server error"
    assert exc_info.value.response_text == "Server error"


def test_unexpected_error():
    """Test handling of unexpected errors"""
    client = MockSyncClient()
    client._http.request.side_effect = Exception("Connection failed")

    with pytest.raises(HubAPIError) as exc_info:
        client.get("/test")

    assert isinstance(exc_info.value, HubAPIError)
    assert "Connection failed" in exc_info.value.message


def test_error_message_extraction():
    """Test the error message extraction helper method"""
    client = MockSyncClient()

    # Test with message in JSON
    response = Mock()
    response.json.return_value = {"message": "Custom error"}
    assert client._extract_error_message(response, "Default error") == "Custom error"

    # Test with no message in JSON
    response.json.return_value = {"foo": "bar"}
    assert client._extract_error_message(response, "Default error") == "Default error"

    # Test with invalid JSON
    response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
    assert client._extract_error_message(response, "Default error") == "Default error"


def test_validation_errors_extraction():
    """Test the validation errors extraction helper method"""
    client = MockSyncClient()

    # Test with both message and fields
    response = Mock()
    response.json.return_value = {
        "message": "Validation failed",
        "fields": {"name": "Required"},
    }
    message, fields = client._extract_validation_errors(response)
    assert message == "Validation failed"
    assert "Required" in fields

    # Test with only message
    response.json.return_value = {"message": "Validation failed"}
    message, fields = client._extract_validation_errors(response)
    assert message == "Validation failed"
    assert fields == ""

    # Test with invalid JSON
    response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
    message, fields = client._extract_validation_errors(response)
    assert message == "Validation error: please check your request"
    assert fields == ""


def test_cast_data_error():
    """Test handling of errors during data casting"""
    client = MockSyncClient()
    response = Mock()
    response.status_code = 200
    response.text = '{"data": "test"}'
    response.json.return_value = {"data": "test"}
    client._http.request.return_value = response

    # Mock _cast_data_to to raise an exception
    cast_to_mock = Mock()
    cast_to_mock.from_dict.side_effect = ValueError("Invalid data format")
    client._cast_data_to = Mock(side_effect=ValueError("Invalid data format"))

    with pytest.raises(HubAPIError) as exc_info:
        client.get("/test", cast_to=cast_to_mock)

    assert isinstance(exc_info.value, HubAPIError)
    assert "Error casting API response data" in exc_info.value.message
    assert "Invalid data format" in exc_info.value.message
    assert exc_info.value.status_code == 200
    assert exc_info.value.response_text == '{"data": "test"}'
