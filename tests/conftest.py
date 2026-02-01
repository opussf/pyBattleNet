"""
Shared pytest fixtures and configuration
"""
import pytest


@pytest.fixture
def sample_api_response():
    """Fixture providing a sample API response"""
    return {
        "status": "success",
        "data": {
            "character": {
                "name": "TestHero",
                "level": 60,
                "realm": "TestRealm"
            }
        }
    }


@pytest.fixture
def mock_api_client():
    """Fixture providing a mock API client"""
    # Return a configured mock or test instance
    pass


@pytest.fixture
def sample_credentials():
    """Fixture for test credentials"""
    return {
        "client_id": "test_client_id",
        "client_secret": "test_client_secret"
    }