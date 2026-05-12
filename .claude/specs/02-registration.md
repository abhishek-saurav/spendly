# Spec: Registration

## Overview
Implement functional user registration so visitors can create a Spendly account.
The `/register` route currently returns a static template; this step wires it up
to a `POST` handler that validates input, hashes the password, inserts the user
into the database, and redirects to the login page on success. This is the first
step that involves user-generated data flowing into the database.

## Depends on
- Step 01 — Database Setup (users table and `get_db` must exist)

## Routes
- `GET  /register` — show registration form — public
- `POST /register` — handle form submission, create user account — public

## Database changes
No new tables or columns. Uses the existing `users` table:
- `id`, `name`, `email`, `password_hash`, `created_at`

A new helper function `create_user(name, email, password_hash)` should be added
to `database/db.py` to keep SQL out of `app.py`.

## Templates
- **Modify:** `templates/register.html`
  - Already renders `{{ error }}` — no structural change needed
  - Confirm form `action="/register"` and `method="POST"` are present (they are)

## Files to change
- `app.py` — replace stub `GET /register` with dual GET/POST handler; add imports
- `database/db.py` — add `create_user()` function

## Files to create
No new files.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never string-format SQL
- Passwords hashed with `werkzeug.security.generate_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Import `request`, `redirect`, `url_for`, `session` from `flask`
- On duplicate email (UNIQUE constraint violation), catch the `sqlite3.IntegrityError`
  and re-render the form with `error="An account with that email already exists."`
- Validate server-side: name non-empty, valid email format, password ≥ 8 characters
- After successful registration, redirect to `/login` with a success flash or query
  param so the login page can show a confirmation message (e.g. `?registered=1`)
- Do not auto-login the user after registration — that belongs to Step 3 (Login)
- Strip whitespace from `name` and `email` before storing

## Definition of done
- [ ] `GET /register` renders the registration form
- [ ] Submitting with valid data inserts a new row into `users` with a hashed password
- [ ] Submitting with an already-registered email shows an inline error on the form
- [ ] Submitting with a password shorter than 8 characters shows a validation error
- [ ] Submitting with an empty name shows a validation error
- [ ] Successful registration redirects to `/login`
- [ ] Password is never stored in plain text (verify in `spendly.db`)
- [ ] Multiple registrations with different emails all succeed independently
