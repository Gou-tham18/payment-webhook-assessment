import sqlite3
from datetime import datetime

from .config import DB_PATH


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS orders ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, event_id TEXT, payment_id TEXT, "
        "customer_email TEXT, amount REAL, status TEXT, created_at TEXT)"
    )
    return conn


def save_order(event_id, payment_id, email, amount):
    conn = get_conn()
    conn.execute(
        "INSERT INTO orders (event_id, payment_id, customer_email, amount, status, created_at) "
        "VALUES (?, ?, ?, ?, 'paid', ?)",
        (event_id, payment_id, email, amount, datetime.utcnow().isoformat()),
    )
    conn.commit()


def mark_refunded(payment_id):
    conn = get_conn()
    conn.execute("UPDATE orders SET status = 'refunded' WHERE payment_id = ?", (payment_id,))
    conn.commit()


def list_orders():
    conn = get_conn()
    rows = conn.execute(
        "SELECT payment_id, customer_email, amount, status FROM orders ORDER BY id"
    ).fetchall()
    return [
        {"payment_id": r[0], "customer_email": r[1], "amount": r[2], "status": r[3]}
        for r in rows
    ]
