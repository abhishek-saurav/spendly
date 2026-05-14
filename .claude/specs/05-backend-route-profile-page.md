# Spec: Backend Route for Profile Page

## Overview
Implement the backend logic for the `/profile` route in `app.py`. This step wires
together the database helper functions added in Step 04 with a dual GET/POST route
that lets authenticated users view their account details and update their display
name or password. It also establishes the auth-guard pattern (redirect to `/login`
when no session) that all future protected routes will follow.

## Depends on
- Step 01 — Database Setup (`users` and `expenses` tables, `get_db`)
- Step 02 — Registration (`create_user`, users table populated)
- Step 03 — Login and Logout (session with `user_id` and `user_name`)
- Step 04 — Profile Page (template `profile.html`, DB helpers `get_user_by_id`,
  `update_user`, `get_expense_stats`)

## Routes
- `GET  /profile` — render profile page with user info and expense stats — logged-in only
- `POST /profile` — handle name update and optional password change — logged-in only

## Database changes
No database changes. All required helper functions (`get_user_by_id`, `update_user`,
`get_expense_stats`) were added to `database/db.py` in Step 04.

## Templates
- **Modify:** None — `templates/profile.html` already exists from Step 04.

## Files to change
- `app.py` — replace the stub `GET /profile` with a full GET/POST handler; import
  `get_user_by_id`, `update_user`, `get_expense_stats` from `database.db`

## Files to create
No new files.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never string-format SQL
- Passwords hashed with `werkzeug.security.generate_password_hash`; verified with
  `check_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Redirect unauthenticated requests to `/login` (check `session.get("user_id")`)
- Name field: strip whitespace, must be non-empty
- Password change is optional — only apply if the new password field is non-empty;
  if provided, require a matching confirm-password field and enforce ≥ 8 characters
- After a successful update, re-render the profile page with
  `success="Profile updated."` — do not redirect (avoids form-resubmit)
- Refresh `session["user_name"]` immediately after a name update so the navbar
  reflects the change without requiring a new login
- `get_expense_stats` must return `{"total_count": 0, "total_amount": 0.0}` when
  the user has no expenses (never return None)

## Definition of done
- [ ] `GET /profile` redirects to `/login` when not authenticated
- [ ] `GET /profile` renders `profile.html` for a logged-in user with name, email,
      and member-since date populated
- [ ] Profile page shows total expense count and total amount spent
- [ ] Submitting the form with a new name updates it in the database and refreshes
      the navbar immediately (no re-login required)
- [ ] Submitting the form with a new password (matching confirm field) updates the
      password hash in the database
- [ ] Submitting with a new password shorter than 8 characters shows an inline error
- [ ] Submitting with mismatched password fields shows an inline error
- [ ] Submitting with an empty name shows an inline error
- [ ] Leaving the password field blank performs a name-only update without error
- [ ] A success message appears after a valid update
