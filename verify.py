"""
Manual verification curls — run against the dev server (python app.py):

    # 1. Unauthenticated GET /tasks -> expect 401
    curl -i http://127.0.0.1:5000/tasks

    # 2. Login to obtain a token
    curl -i -X POST http://127.0.0.1:5000/login \
        -H "Content-Type: application/json" \
        -d '{"email": "you@example.com", "password": "yourpass"}'

    # 3. Authenticated GET /tasks, using the token from step 2
    curl -i http://127.0.0.1:5000/tasks \
        -H "Authorization: Bearer <paste-token-here>"
"""

from app import create_app


c = create_app().test_client()

def create_signup_user(): 
    resp = c.post("/signup", json={"email": "a@b.com", "password": "hunter2"})
    assert resp.status_code == 201

def login_user():
    resp = c.post("/login", json={"email": "a@b.com", "password": "hunter2"})
    assert resp.status_code == 200

def add_user_task():
    resp = c.post("/login", json={"email": "a@b.com", "password": "hunter2"})
    assert resp.status_code == 200, resp.json
    assert resp.json is not None, "login returned no body"
    token = resp.json.get("access_token")

    r1 = c.post("/tasks", json={"title": "test"}, headers={"Authorization": f"Bearer {token}"})
    assert r1.status_code == 201, r1.json

    r2 = c.post("/tasks", json={"title": "   "}, headers={"Authorization": f"Bearer {token}"})
    assert r2.status_code == 400, r2.json


add_user_task()
