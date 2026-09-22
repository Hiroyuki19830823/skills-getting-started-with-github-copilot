from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_and_unregister_activity_participant():
    # Arrange
    activity_name = "Chess Club"
    email = "aaa-test-student@mergington.edu"

    activity = client.get("/activities").json()[activity_name]
    if email in activity["participants"]:
        client.delete(f"/activities/{activity_name}/participants?email={email}")

    # Act: sign up
    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert: signup succeeds and participant is present
    assert signup_response.status_code == 200
    assert signup_response.json()["message"] == f"Signed up {email} for {activity_name}"

    updated_activity = client.get("/activities").json()[activity_name]
    assert email in updated_activity["participants"]

    # Act: unregister
    delete_response = client.delete(f"/activities/{activity_name}/participants?email={email}")

    # Assert: participant is removed
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == f"Removed {email} from {activity_name}"

    final_activity = client.get("/activities").json()[activity_name]
    assert email not in final_activity["participants"]


def test_duplicate_signup_returns_400():
    # Arrange
    activity_name = "Chess Club"
    email = "duplicate-test-student@mergington.edu"

    activity = client.get("/activities").json()[activity_name]
    if email in activity["participants"]:
        client.delete(f"/activities/{activity_name}/participants?email={email}")

    # Act
    first_signup = client.post(f"/activities/{activity_name}/signup?email={email}")
    duplicate_signup = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert first_signup.status_code == 200
    assert duplicate_signup.status_code == 400
    assert duplicate_signup.json()["detail"] == "Student already signed up for this activity"

    client.delete(f"/activities/{activity_name}/participants?email={email}")
