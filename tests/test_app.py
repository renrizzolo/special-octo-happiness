def test_root_redirect(client):
    """Test that GET / redirects to /static/index.html."""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_success(client):
    """Test retrieving all extracurricular activities."""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data

    chess = data["Chess Club"]
    assert "description" in chess
    assert "schedule" in chess
    assert "max_participants" in chess
    assert "participants" in chess
    assert isinstance(chess["participants"], list)


def test_signup_success(client):
    """Test successfully signing up for an activity."""
    activity_name = "Soccer Team"
    email = "new_student@mergington.edu"

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}

    # Verify student is now listed in the activity participants
    activities_response = client.get("/activities")
    assert email in activities_response.json()[activity_name]["participants"]


def test_signup_duplicate_email(client):
    """Test signing up an email that is already registered returns 400."""
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": existing_email}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_nonexistent_activity(client):
    """Test signing up for a non-existent activity returns 404."""
    response = client.post(
        "/activities/NonExistentActivity/signup",
        params={"email": "student@mergington.edu"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_success(client):
    """Test successfully unregistering a participant."""
    activity_name = "Chess Club"
    participant_email = "michael@mergington.edu"

    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": participant_email}
    )
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {participant_email} from {activity_name}"}

    # Verify student is removed from the activity participants
    activities_response = client.get("/activities")
    assert participant_email not in activities_response.json()[activity_name]["participants"]


def test_unregister_not_registered(client):
    """Test unregistering a participant not enrolled in the activity returns 404."""
    activity_name = "Chess Club"
    not_enrolled_email = "not_enrolled@mergington.edu"

    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": not_enrolled_email}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found for this activity"


def test_unregister_nonexistent_activity(client):
    """Test unregistering from a non-existent activity returns 404."""
    response = client.delete(
        "/activities/NonExistentActivity/unregister",
        params={"email": "student@mergington.edu"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
