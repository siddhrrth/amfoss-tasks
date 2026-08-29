import sqlite3
import os

os.makedirs("database", exist_ok=True)
# Creates the database folder if it doesn't already exist.

conn = sqlite3.connect("database/berry.db")
# Connects to the SQLite database.

cursor = conn.cursor()
print("Database connected successfully..")


def create_tables():
    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        wallet INTEGER DEFAULT 500,
        last_daily TEXT
    )
    """)

    # Inventory table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        item_name TEXT NOT NULL,
        quantity INTEGER DEFAULT 1,
        active INTEGER DEFAULT 1,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """)

    # Transaction history table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        action TEXT NOT NULL,
        amount INTEGER NOT NULL,
        description TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """)

    conn.commit()


create_tables()


def get_user(user_id):
    cursor.execute(
        "SELECT * FROM users WHERE user_id = ?",
        (user_id,)
    )

    user = cursor.fetchone()

    if user is None:
        cursor.execute(
            "INSERT INTO users (user_id) VALUES (?)",
            (user_id,)
        )
        conn.commit()

        cursor.execute(
            "SELECT * FROM users WHERE user_id = ?",
            (user_id,)
        )
        user = cursor.fetchone()

    return user


def get_wallet(user_id):
    get_user(user_id)

    cursor.execute(
        "SELECT wallet FROM users WHERE user_id = ?",
        (user_id,)
    )

    return cursor.fetchone()[0]


def update_wallet(user_id, amount):
    cursor.execute(
        "UPDATE users SET wallet = ? WHERE user_id = ?",
        (amount, user_id)
    )
    conn.commit()


def add_wallet(user_id, amount):
    current = get_wallet(user_id)
    update_wallet(user_id, current + amount)


def update_last_daily(user_id, time):
    cursor.execute(
        "UPDATE users SET last_daily = ? WHERE user_id = ?",
        (time, user_id)
    )
    conn.commit()


def get_last_daily(user_id):
    get_user(user_id)

    cursor.execute(
        "SELECT last_daily FROM users WHERE user_id = ?",
        (user_id,)
    )

    return cursor.fetchone()[0]


def get_top_users():
    cursor.execute("""
        SELECT user_id, wallet
        FROM users
        ORDER BY wallet DESC
        LIMIT 5
    """)

    return cursor.fetchall()


def add_item(user_id, item_name):
    cursor.execute(
        """
        SELECT quantity
        FROM inventory
        WHERE user_id = ? AND item_name = ? AND active = 1
        """,
        (user_id, item_name)
    )

    item = cursor.fetchone()

    if item:
        cursor.execute(
            """
            UPDATE inventory
            SET quantity = quantity + 1
            WHERE user_id = ? AND item_name = ? AND active = 1
            """,
            (user_id, item_name)
        )
    else:
        cursor.execute(
            """
            INSERT INTO inventory (user_id, item_name, quantity, active)
            VALUES (?, ?, 1, 1)
            """,
            (user_id, item_name)
        )

    conn.commit()


def get_inventory(user_id):
    cursor.execute(
        """
        SELECT item_name, quantity, active
        FROM inventory
        WHERE user_id = ?
        """,
        (user_id,)
    )

    return cursor.fetchall()


def raid_transfer(attacker_id, target_id, amount):
    attacker_balance = get_wallet(attacker_id)
    target_balance = get_wallet(target_id)

    if target_balance < amount:
        amount = target_balance

    update_wallet(target_id, target_balance - amount)
    update_wallet(attacker_id, attacker_balance + amount)

    return amount


def add_history(user_id, action, amount, description):
    cursor.execute(
        """
        INSERT INTO history
        (user_id, action, amount, description, created_at)
        VALUES (?, ?, ?, ?, datetime('now'))
        """,
        (user_id, action, amount, description)
    )

    conn.commit()


def get_history(user_id, limit=10):
    cursor.execute(
        """
        SELECT action, amount, description, created_at
        FROM history
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (user_id, limit)
    )

    return cursor.fetchall()


print("Database and tables created successfully!")