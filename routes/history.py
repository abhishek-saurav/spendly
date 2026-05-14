import sqlite3

from flask import Blueprint, jsonify, session

history_bp = Blueprint("history", __name__, url_prefix="/profile")

DB_PATH = "spendly.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def get_user_expenses(user_id):
    conn = get_db()
    rows = conn.execute(
        """
        SELECT id, amount, category, date, description, created_at
        FROM expenses
        WHERE user_id = ?
        ORDER BY date DESC, created_at DESC
        """,
        (user_id,),
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


@history_bp.route("/history", methods=["GET"])
def history():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    expenses = get_user_expenses(user_id)
    return jsonify({"expenses": expenses})
