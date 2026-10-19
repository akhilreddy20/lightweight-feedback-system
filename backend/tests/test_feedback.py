from conftest import register, token_for

FEEDBACK = {"strengths": "Ownership", "areas_to_improve": "Testing", "sentiment": "positive"}


def setup_team(client):
    register(client, "manager", "manager")
    register(client, "emp1", "employee")
    register(client, "emp2", "employee")
    m = token_for(client, "manager")
    team = client.get("/feedback/team", headers=m).json()
    ids = {e["username"]: e["_id"] for e in team}
    return m, token_for(client, "emp1"), token_for(client, "emp2"), ids


def test_manager_submits_and_employee_reads(client):
    m, e1, _, ids = setup_team(client)
    res = client.post(f"/feedback/{ids['emp1']}", json=FEEDBACK, headers=m)
    assert res.status_code == 200, res.text

    mine = client.get("/feedback/", headers=e1).json()
    assert len(mine) == 1
    assert mine[0]["strengths"] == "Ownership"
    assert mine[0]["acknowledged"] is False
    assert "timestamp" in mine[0]


def test_employees_cannot_submit_or_list_team(client):
    _, e1, _, ids = setup_team(client)
    assert client.post(f"/feedback/{ids['emp2']}", json=FEEDBACK, headers=e1).status_code == 403
    assert client.get("/feedback/team", headers=e1).status_code == 403


def test_employee_cannot_read_someone_elses_history(client):
    m, _, e2, ids = setup_team(client)
    client.post(f"/feedback/{ids['emp1']}", json=FEEDBACK, headers=m)
    assert client.get(f"/feedback/{ids['emp1']}", headers=e2).status_code == 403


def test_employee_cannot_acknowledge_someone_elses_feedback(client):
    m, e1, e2, ids = setup_team(client)
    fb_id = client.post(f"/feedback/{ids['emp1']}", json=FEEDBACK, headers=m).json()["id"]

    assert client.patch(f"/feedback/{fb_id}/acknowledge", headers=e2).status_code == 404
    assert client.patch(f"/feedback/{fb_id}/acknowledge", headers=e1).status_code == 200


def test_invalid_sentiment_rejected(client):
    m, _, _, ids = setup_team(client)
    bad = {**FEEDBACK, "sentiment": "angry"}
    assert client.post(f"/feedback/{ids['emp1']}", json=bad, headers=m).status_code == 422


def test_manager_can_edit_own_feedback(client):
    m, _, _, ids = setup_team(client)
    fb_id = client.post(f"/feedback/{ids['emp1']}", json=FEEDBACK, headers=m).json()["id"]
    res = client.patch(f"/feedback/{fb_id}/edit", json={**FEEDBACK, "sentiment": "neutral"}, headers=m)
    assert res.status_code == 200
