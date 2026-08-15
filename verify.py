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

# Login returns a token (resp.json["access_token"]).
def login_user():
    resp = c.post("/login", json={"email": "a@b.com", "password": "scrypt:32768:8:1$4bvCZTaXt8nXcIFM$b43012a55bef55374841f5dd7ec87788d38fff46afa47c8f8fd1d3fad5c54648cbec804b4c2150e9034e16941c910a669c0f5badd15bc52bc1752fe964eab910"})
# POST /tasks without a token → 401 (the new @jwt_required doing its job).
# POST /tasks with token → 201, task exists.
# GET /tasks/<user_id> returns only that user's tasks.