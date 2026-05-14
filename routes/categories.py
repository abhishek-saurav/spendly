import sqlite3
from flask import Blueprint, jsonify, session

DB_PATH = "spendly.db"

categories_bp = Blueprint("categories_bp", __name__, url_prefix="/profile")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def get_expenses_by_category(user_id):
    conn = get_db()
    try:
        cursor = conn.execute(
            """
            SELECT category,
                   COUNT(*) AS count,
                   COALESCE(SUM(amount), 0.0) AS total
            FROM expenses
            WHERE user_id = ?
            GROUP BY category
            ORDER BY total DESC
            """,
            (user_id,),
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows] if rows else []
    finally:
        conn.close()


@categories_bp.route("/categories", methods=["GET"])
def categories():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = get_expenses_by_category(user_id)
    return jsonify({"categories": data})
