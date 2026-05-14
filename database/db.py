import sqlite3
from werkzeug.security import generate_password_hash

DB_PATH = "spendly.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            email         TEXT    NOT NULL UNIQUE,
            password_hash TEXT    NOT NULL,
            created_at    TEXT    DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL REFERENCES users(id),
            amount      REAL    NOT NULL,
            category    TEXT    NOT NULL,
            date        TEXT    NOT NULL,
            description TEXT,
            created_at  TEXT    DEFAULT (datetime('now'))
        );
    """)
    conn.commit()
    conn.close()


def create_user(name, email, password_hash):
    conn = get_db()
    conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        (name, email, password_hash),
    )
    conn.commit()
    conn.close()


def get_user_by_email(email):
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE email = ?", (email,)
    ).fetchone()
    conn.close()
    return user


def get_user_by_id(user_id):
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    conn.close()
    return user


def update_user(user_id, name, password_hash):
    conn = get_db()
    if password_hash is not None:
        conn.execute(
            "UPDATE users SET name = ?, password_hash = ? WHERE id = ?",
            (name, password_hash, user_id),
        )
    else:
        conn.execute(
            "UPDATE users SET name = ? WHERE id = ?",
            (name, user_id),
        )
    conn.commit()
    conn.close()


def get_expense_stats(user_id):
    conn = get_db()
    row = conn.execute(
        "SELECT COUNT(*) AS total_count, COALESCE(SUM(amount), 0.0) AS total_amount"
        " FROM expenses WHERE user_id = ?",
        (user_id,),
    ).fetchone()
    conn.close()
    if row is None:
        return {"total_count": 0, "total_amount": 0.0}
    return {"total_count": row["total_count"], "total_amount": row["total_amount"]}


def seed_db():
    conn = get_db()
    if conn.execute("SELECT 1 FROM users LIMIT 1").fetchone():
        conn.close()
        return

    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", generate_password_hash("demo123")),
    )
    user_id = cursor.lastrowid

    expenses = [
        (user_id, 12.50,  "Food",          "2026-05-01", "Lunch at cafe"),
        (user_id, 35.00,  "Transport",     "2026-05-02", "Monthly bus pass"),
        (user_id, 120.00, "Bills",         "2026-05-03", "Electricity bill"),
        (user_id, 45.00,  "Health",        "2026-05-05", "Pharmacy"),
        (user_id, 18.00,  "Entertainment", "2026-05-07", "Movie ticket"),
        (user_id, 60.00,  "Shopping",      "2026-05-08", "Clothes"),
        (user_id, 9.99,   "Other",         "2026-05-10", "Miscellaneous"),
        (user_id, 22.00,  "Food",          "2026-05-11", "Grocery run"),
    ]
    cursor.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        expenses,
    )
    conn.commit()
    conn.close()
