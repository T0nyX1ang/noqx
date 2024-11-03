"""Configurations for the tests."""

from typing import Iterator

import pytest
from starlette.config import environ
from starlette.testclient import TestClient

from noqx import app

environ["DEBUG"] = "TRUE"


@pytest.fixture()
def client() -> Iterator[TestClient]:
    """Make a client fixture available to test cases."""
    with TestClient(app) as test_client:
        yield test_client
