- [x] docstring
- [ ] implement all the fixes
    - [x] D2/D3 — GET /tasks (public, returns everything) and GET /tasks/<user_id> (public, trusts a URL param) bypass the scoping you just built.
    - [x] D4 — your live task_manager.db still predates the user_id column; it'll crash on first insert.
    - [x] D5 — DB errors still masquerade as 404s.
- [ ] complete 100% jwt ownership and login stuff

### Optimizations
- [ ] D6 + minors — response shape, unu imposedrts, 3.11 f-string portability, stale docstrings.