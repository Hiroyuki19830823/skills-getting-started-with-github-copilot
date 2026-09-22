from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_delete_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "new-student@mergington.edu"

    activity = client.get("/activities").json()[activity_name]
    if email in activity["participants"]:
        client.delete(f"/activities/{activity_name}/participants?email={email}")

    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200

    delete_response = client.delete(f"/activities/{activity_name}/participants?email={email}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == f"Removed {email} from {activity_name}"

    updated_activity = client.get("/activities").json()[activity_name]
    assert email not in updated_activity["participants"]
