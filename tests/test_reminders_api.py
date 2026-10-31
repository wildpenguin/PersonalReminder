from datetime import datetime, timedelta

import pytest

REMINDER = {
    "due": "2026-10-30T09:00:00+02:00",
    "title": "Standup",
    "message": "Daily meeting",
}


def test_list_is_empty_on_fresh_database(client):
    response = client.get("/reminders")

    assert response.status_code == 200
    assert response.json() == []


def test_create_returns_reminder_with_id(client):
    response = client.post("/reminders", json=REMINDER)

    assert response.status_code == 201
    body = response.json()
    assert isinstance(body["id"], int)
    assert body["title"] == "Standup"
    assert body["message"] == "Daily meeting"


def test_create_applies_defaults(client):
    body = client.post("/reminders", json=REMINDER).json()

    assert body["repeat"] is False
    assert body["priority"] == "normal"
    assert body["enabled"] is True


def test_created_reminder_is_listed(client):
    created = client.post("/reminders", json=REMINDER).json()

    response = client.get("/reminders")

    assert response.status_code == 200
    listed = response.json()
    assert len(listed) == 1
    assert listed[0]["id"] == created["id"]
    assert listed[0]["title"] == created["title"]
    assert listed[0]["message"] == created["message"]


def test_each_reminder_gets_its_own_id(client):
    first = client.post("/reminders", json=REMINDER).json()
    second = client.post("/reminders", json={**REMINDER, "title": "Lunch"}).json()

    assert first["id"] != second["id"]
    titles = {reminder["title"] for reminder in client.get("/reminders").json()}
    assert titles == {"Standup", "Lunch"}


def test_due_is_returned_in_utc_at_the_same_moment(client):
    client.post("/reminders", json=REMINDER)

    due = datetime.fromisoformat(client.get("/reminders").json()[0]["due"])

    assert due.utcoffset() == timedelta(0)
    assert due == datetime.fromisoformat(REMINDER["due"])


def test_all_fields_are_saved(client):
    client.post("/reminders", json={**REMINDER, "repeat": True, "priority": "high"})

    saved = client.get("/reminders").json()[0]

    assert saved["repeat"] is True
    assert saved["priority"] == "high"


def test_disabled_reminders_are_not_listed(client):
    client.post("/reminders", json={**REMINDER, "enabled": False})

    assert client.get("/reminders").json() == []


@pytest.mark.parametrize(
    "body",
    [
        {**REMINDER, "due": "2026-10-30T09:00:00"},
        {**REMINDER, "due": "not a date"},
        {**REMINDER, "priority": "urgent"},
        {"due": REMINDER["due"], "message": "No title"},
    ],
    ids=["due-without-timezone", "due-not-a-date", "unknown-priority", "missing-title"],
)
def test_create_rejects_invalid_input(client, body):
    response = client.post("/reminders", json=body)

    assert response.status_code == 422
