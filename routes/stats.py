import sqlite3

from flask import Blueprint, jsonify, session

stats_bp = Blueprint("stats_bp", __name__, url_prefix="/profile")

DB_PATH = "spendly.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def get_monthly_stats(user_id):
    conn = get_db()
    try:
        cursor = conn.execute(
            """
            SELECT strftime('%Y-%m', date) AS month,
                   COUNT(*) AS count,
                   COALESCE(SUM(amount), 0.0) AS total
            FROM expenses
            WHERE user_id = ?
            GROUP BY month
            ORDER BY month DESC
            """,
            (user_id,),
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows] if rows else []
    finally:
        conn.close()


@stats_bp.route("/summary", methods=["GET"])
def summary():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    monthly = get_monthly_stats(user_id)
    return jsonify({"monthly": monthly})
