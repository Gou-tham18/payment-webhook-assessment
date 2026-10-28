
import sqlite3
from datetime import datetime, timezone
from contextlib import closing

from .config import DB_PATH


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS orders ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, event_id TEXT, payment_id TEXT, "
            "customer_email TEXT, amount REAL, status TEXT, created_at TEXT)"
        )
        return conn
    except Exception:
        conn.close()
        raise


def save_order(event_id, payment_id, email, amount):
    with closing(get_conn()) as conn:
        with conn:
            conn.execute(
                "INSERT INTO orders "
                "(event_id, payment_id, customer_email, amount, status, created_at) "
                "VALUES (?, ?, ?, ?, 'paid', ?)",
                (
                    event_id,
                    payment_id,
                    email,
                    amount,
                    datetime.now(timezone.utc).isoformat(),
                ),
            )


def mark_refunded(payment_id):
    with closing(get_conn()) as conn:
        with conn:
            conn.execute(
                "UPDATE orders SET status = 'refunded' WHERE payment_id = ?",
                (payment_id,),
            )


def list_orders():
    with closing(get_conn()) as conn:
        rows = conn.execute(
            "SELECT payment_id, customer_email, amount, status "
            "FROM orders ORDER BY id"
        ).fetchall()

    return [
        {
            "payment_id": row[0],
            "customer_email": row[1],
            "amount": row[2],
            "status": row[3],
        }
        for row in rows
    ]
