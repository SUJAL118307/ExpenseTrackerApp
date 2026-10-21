
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "expenses.db"


def connect():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with connect() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                amount_paise INTEGER NOT NULL CHECK (amount_paise > 0),
                transaction_type TEXT NOT NULL
                    CHECK (transaction_type IN ('Income', 'Expense')),
                category TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT
                    (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime'))
            )
        """)


def add_transaction(title, amount_paise, transaction_type, category):
    with connect() as connection:
        connection.execute(
            """
            INSERT INTO transactions
                (title, amount_paise, transaction_type, category)
            VALUES (?, ?, ?, ?)
            """,
            (title, amount_paise, transaction_type, category),
        )


def get_transactions():
    with connect() as connection:
        rows = connection.execute(
            """
            SELECT id, title, amount_paise, transaction_type,
                   category, created_at
            FROM transactions
            ORDER BY id DESC
            """
        ).fetchall()
        return [dict(row) for row in rows]


def delete_transaction(transaction_id):
    with connect() as connection:
        connection.execute(
            "DELETE FROM transactions WHERE id = ?",
            (transaction_id,),
        )

def update_transaction(transaction_id, title, amount_paise,
                       transaction_type, category):
    with connect() as connection:
        connection.execute(
            """
            UPDATE transactions
            SET title = ?,
                amount_paise = ?,
                transaction_type = ?,
                category = ?
            WHERE id = ?
            """,
            (
                title,
                amount_paise,
                transaction_type,
                category,
                transaction_id,
            ),
        )
