## task-manager
### task manager api - python application

**simple overview**: simple api to manage tasks. users can create, update, and organize tasks securely with user login. building to learn how to handle databases and secure user access.

**technologies used**

- Python (Flask Framework)
- SQLite (Database)
- JWT Authentication
- RESTful API Design
- CRUD Operations
- User Authentication


**api responsibilities:**

- [ ] *User Management*:
    - Sign up and log in to get a JWT token.
    - Secure API with JWT.

- [ ] *Task Management*:
    - Create tasks (title, description, category).
    - View all tasks or filter by status/category.
    - Update or delete tasks by ID.

- [ ] *Task Operations (CRUD)*:
    - Create a new task: Allow users to add a task with a title, description, and optional category (e.g., work, personal).
    - Read tasks:
        - Return all tasks belonging to the authenticated user.
        - Filter by status (e.g., completed or pending) or category.
        - Retrieve a single task by its ID.
        - Update a task: Modify task details (title, description, category) or mark it as completed/pending using its ID.
        - Delete a task: Remove a task based on its ID.


**learning pathway** *(build manually, layer by layer)*

- [x] **Step 1 — Hello Flask** *(no database, no auth)*
    - [x] Add a health route: `GET /health` → `{"status": "ok"}`
    - [x] Run the app locally and confirm JSON responses work

- [ ] **Step 2 — In-memory tasks** *(no database yet)*
    - [ ] Store tasks in a Python list or dict
    - [ ] `POST /tasks` — create a task
    - [ ] `GET /tasks` — list all tasks
    - [ ] `GET /tasks/<id>` — get one task
    - [ ] `PUT /tasks/<id>` — update a task
    - [ ] `DELETE /tasks/<id>` — delete a task
    - [ ] Notice: data is lost on restart; no user isolation yet

- [ ] **Step 3 — SQLite manually** *(built-in `sqlite3`, no ORM)*
    - [ ] Create `tasks.db` and a `tasks` table with SQL
    - [ ] Use parameterized queries for all CRUD operations
    - [ ] Wire SQLite into the existing task routes

- [ ] **Step 4 — Users** *(still no JWT)*
    - [ ] Create a `users` table (id, username, password_hash)
    - [ ] Signup: hash passwords with `werkzeug.security.generate_password_hash`
    - [ ] Login: verify with `check_password_hash`
    - [ ] Return a simple login response (e.g. user id), not a token yet

- [ ] **Step 5 — Scope tasks to users**
    - [ ] Add `user_id` to the tasks table
    - [ ] Filter every task query by the logged-in user
    - [ ] Confirm users cannot access each other's tasks

- [ ] **Step 6 — JWT auth**
    - [ ] Issue a JWT on successful login
    - [ ] Protect task routes with `Authorization: Bearer <token>`
    - [ ] Decode the token to get `user_id` on each request
    - [ ] Reject requests with missing or invalid tokens

- [ ] **Step 7 — Filters and polish**
    - [ ] Filter tasks by status (completed / pending)
    - [ ] Filter tasks by category
    - [ ] Mark tasks completed or pending via update


**packages by phase**

| Phase | Packages |
|-------|----------|
| Steps 1–3 | `Flask` only |
| Step 4 | `Flask` + Werkzeug *(included with Flask)* |
| Step 6 | Add `PyJWT` or `Flask-JWT-Extended` |

Skip Flask-SQLAlchemy until raw SQL feels comfortable — then rebuild with an ORM to see what it automates.


**suggested folder structure** *(keep flat at first)*

```
task-manager/
├── app.py          # routes + app setup
├── db.py           # sqlite connection helpers
├── auth.py         # signup, login, jwt helpers
├── requirements.txt
└── tasks.db        # created at runtime
```


**self-check** *(can you explain these without looking at code?)*

- [ ] What happens when I hit `POST /tasks`?
- [ ] Where is the password stored, and in what form?
- [ ] How does the server know which user's tasks to return?
- [ ] What breaks if I send a request without a token?
