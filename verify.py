from app import create_app
c = create_app().test_client()
c.post("/signup", json={"email": "a@b.com", "password": "hunter2"})
