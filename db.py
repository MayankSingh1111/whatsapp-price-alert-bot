# db.py
import sqlite3

DB_NAME = "price_tracker.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    """Create tables if they do not exist."""
    with get_connection() as conn:
        cur = conn.cursor()

        # Products table
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                url TEXT NOT NULL,
                target_price REAL NOT NULL,
                last_price REAL,
                currency TEXT DEFAULT 'INR',
                active INTEGER DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            """
        )

        # Price history table
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                price REAL NOT NULL,
                currency TEXT DEFAULT 'INR',
                checked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(product_id) REFERENCES products(id)
            );
            """
        )

        conn.commit()


def add_product(name: str, url: str, target_price: float, currency: str = "INR"):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO products (name, url, target_price, currency)
            VALUES (?, ?, ?, ?)
            """,
            (name, url, target_price, currency),
        )
        conn.commit()


def list_products(active_only: bool = True):
    """Return list of products (rows)."""
    with get_connection() as conn:
        cur = conn.cursor()
        if active_only:
            cur.execute(
                """
                SELECT id, name, url, target_price, last_price, currency, active
                FROM products
                WHERE active = 1
                """
            )
        else:
            cur.execute(
                """
                SELECT id, name, url, target_price, last_price, currency, active
                FROM products
                """
            )
        return cur.fetchall()


def save_price(product_id: int, price: float, currency: str = "INR"):
    """Insert into price_history and update last_price in products."""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO price_history (product_id, price, currency)
            VALUES (?, ?, ?)
            """,
            (product_id, price, currency),
        )
        cur.execute(
            """
            UPDATE products
            SET last_price = ?
            WHERE id = ?
            """,
            (price, product_id),
        )
        conn.commit()


def deactivate_product(product_id: int):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE products
            SET active = 0
            WHERE id = ?
            """,
            (product_id,),
        )
        conn.commit()
