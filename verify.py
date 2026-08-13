from app import create_app
c = create_app().test_client()

def create_signup_user(): 
    resp = c.post("/signup", json={"email": "a@b.com", "password": "hunter2"})
    assert resp.status_code == 201

# Login returns a token (resp.json["access_token"]).
# POST /tasks without a token → 401 (the new @jwt_required doing its job).
# POST /tasks with token → 201, task exists.
# GET /tasks/<user_id> returns only that user's tasks.