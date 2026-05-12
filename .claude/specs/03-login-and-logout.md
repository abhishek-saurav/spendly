# Spec: Login and Logout

## Overview
Implement functional login and logout so registered users can authenticate into
Spendly and end their session. The `/login` route is currently a stub that only
renders a template; this step wires up the `POST` handler to verify credentials,
create a server-side session, and redirect to the dashboard. The `/logout` route
clears the session and redirects to the landing page. This step introduces Flask's
`session` object and the concept of protected routes.

## Depends on
- Step 01 — Database Setup (users table, `get_db` must exist)
- Step 02 — Registration (users must exist in the database to log in)

## Routes
- `GET  /login`  — show login form — public
- `POST /login`  — verify credentials, create session — public
- `GET  /logout` — clear session, redirect to landing — logged-in

## Database changes
No new tables or columns. Reads from the existing `users` table:
- Lookup user by `email`, compare `password_hash` using `werkzeug`.

A new helper function `get_user_by_email(email)` should be added to
`database/db.py` to keep SQL out of `app.py`.

## Templates
- **Modify:** `templates/login.html`
  - Add a `POST` form with `email` and `password` fields if not already present
  - Render `{{ error }}` for invalid credentials
  - Render a success banner when `registered=1` query param is present
  - Form `action="/login"` and `method="POST"` must be set

## Files to change
- `app.py` — replace stub `GET /login` with dual GET/POST handler; implement `logout`; add `secret_key`; add imports
- `database/db.py` — add `get_user_by_email(email)` function

## Files to create
No new files.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never string-format SQL
- Passwords verified with `werkzeug.security.check_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- `app.secret_key` must be set (use a hardcoded dev string for now, e.g. `"spendly-dev-secret"`)
- On successful login, store `session["user_id"]` and `session["user_name"]`
- On failed login (wrong email or wrong password), show the same generic error: `"Invalid email or password."` — do not reveal which field was wrong
- Strip and lowercase the email before lookup
- `logout` must call `session.clear()` before redirecting to `url_for("landing")`
- Do not redirect logged-in users away from `/login` automatically in this step — that guard belongs to a later step
- `GET /logout` is acceptable for this step; no POST-based CSRF protection required yet

## Definition of done
- [ ] `GET /login` renders the login form
- [ ] Submitting valid credentials creates a session and redirects away from `/login`
- [ ] Submitting an unrecognised email shows `"Invalid email or password."` inline
- [ ] Submitting a wrong password shows `"Invalid email or password."` inline
- [ ] After login, `session["user_id"]` contains the correct user's id
- [ ] Visiting `/logout` clears the session and redirects to the landing page
- [ ] After logout, `session.get("user_id")` is `None`
- [ ] Login form shows a success banner when `?registered=1` is present in the URL
- [ ] Demo user (`demo@spendly.com` / `demo123`) can log in successfully
