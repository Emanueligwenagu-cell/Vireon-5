# Ibhotwe Database

This folder contains the SQLite database for the WSU Ibhotwe Food Ordering Platform.

## Database File
- **`ibhotwe.db`**: The SQLite database file storing users, vendors, products, orders, and order items.

## Tables
1. **`users`** — Student and vendor accounts with hashed passwords, roles (`student` or `vendor`), and loyalty points.
2. **`vendors`** — Vendor stalls (e.g., Mama's Kitchen, Kota Corner).
3. **`products`** — Menu items with prices, categories, prep times, and descriptions.
4. **`orders`** — Placed orders with status (`pending`, `preparing`, `ready`, `completed`, `cancelled`), total amount, and timestamps.
5. **`order_items`** — Individual food items linked to each order.

## How It Works
- The database is initialized and managed by `backend/main.py` via Python's built-in `sqlite3`.
- If `ibhotwe.db` is deleted or missing, the backend will automatically re-create and populate it with default demo data on startup.

