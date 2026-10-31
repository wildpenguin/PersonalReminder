import pytest
from fastapi.testclient import TestClient

from reminder import api
from reminder.repositories.reminders import ReminderRepository
from reminder.services.database import Database


@pytest.fixture
def client(tmp_path, monkeypatch):
    """A test client whose API uses a fresh, empty database for each test."""
    db = Database(tmp_path / "test.db")
    monkeypatch.setattr(api, "db", db)
    monkeypatch.setattr(api, "repo", ReminderRepository(db))
    with TestClient(api.app) as client:
        yield client
