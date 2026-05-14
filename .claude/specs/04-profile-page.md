# Spec: Profile Page

## Overview
Implement a profile page at `/profile` where logged-in users can view their
account details (name, email, member-since date) and update their display name
or password. The page also shows a lightweight stats summary — total number of
expenses recorded and total amount spent — giving users a quick sense of their
activity. This is the first authenticated-only view in Spendly; it establishes
the access-control pattern (redirect to `/login` when no session) that all
future protected routes will follow.

## Depends on
- Step 01 — Database Setup (`users` and `expenses` tables, `get_db`)
- Step 02 — Registration (`create_user`, users table populated)
- Step 03 — Login and Logout (session with `user_id` and `user_name`)

## Routes
- `GET  /profile` — show profile page with user info and stats — logged-in only
- `POST /profile` — handle update-name or change-password form submission — logged-in only

## Database changes
No new tables or columns. Two new helper functions should be added to
`database/db.py` to keep SQL out of `app.py`:

- `get_user_by_id(user_id)` — returns a single user row by primary key
- `update_user(user_id, name, password_hash)` — updates name and/or
  password_hash for the given user; pass `None` for fields that should not
  change
- `get_expense_stats(user_id)` — returns a dict with `total_count` (INTEGER)
  and `total_amount` (REAL) for all expenses belonging to the user

## Templates
- **Create:** `templates/profile.html`
  - Extends `base.html`
  - Two sections: "Your account" (read-only info) and "Edit profile" (form)
  - Edit form has: name field (pre-filled), new password field (optional),
    confirm password field, and a submit button
  - Shows `{{ error }}` and `{{ success }}` flash messages inline
  - Shows stats: total expenses count and total amount spent

- **Modify:** `templates/base.html`
  - Add a "Profile" link in the nav alongside the Sign out button when the
    user is logged in: `<a href="{{ url_for('profile') }}">Profile</a>`

## Files to change
- `app.py` — replace stub `GET /profile` with dual GET/POST handler; import
  `get_user_by_id`, `update_user`, `get_expense_stats`
- `database/db.py` — add `get_user_by_id()`, `update_user()`,
  `get_expense_stats()`
- `templates/base.html` — add Profile nav link for logged-in users
- `static/css/style.css` — add profile page styles (`.profile-layout`,
  `.profile-card`, `.profile-stat`, `.form-group`, `.form-label`,
  `.form-input`, `.form-hint`)

## Files to create
- `templates/profile.html`

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never string-format SQL
- Passwords hashed with `werkzeug.security.generate_password_hash`; verified
  with `check_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Redirect unauthenticated requests to `/login` (check `session.get("user_id")`)
- Name field: strip whitespace, must be non-empty
- Password change is optional — only apply if the new password field is
  non-empty; if provided, require a matching confirm-password field and
  enforce ≥ 8 characters
- After a successful update, re-render the profile page with
  `success="Profile updated."` — do not redirect (avoids form-resubmit)
- Refresh `session["user_name"]` immediately after a name update so the
  navbar reflects the change without requiring a new login
- `get_expense_stats` must return `{"total_count": 0, "total_amount": 0.0}`
  when the user has no expenses (never return None)

## Definition of done
- [ ] `GET /profile` redirects to `/login` when not authenticated
- [ ] `GET /profile` renders the profile page for a logged-in user with their
      name, email, and member-since date
- [ ] Profile page shows total expense count and total amount spent
- [ ] Submitting the form with a new name updates it in the database and
      refreshes the navbar immediately (no re-login required)
- [ ] Submitting the form with a new password (matching confirm field) updates
      the password hash in the database
- [ ] Submitting with a new password shorter than 8 characters shows an error
- [ ] Submitting with mismatched password fields shows an error
- [ ] Submitting with an empty name shows an error
- [ ] Leaving the password field blank performs a name-only update (no error)
- [ ] A success message appears after a valid update
