from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr, Field
import sqlite3
import os
import hashlib
import hmac
import secrets
import base64
import json
import time
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"
DATABASE_DIR = PROJECT_ROOT / "database"
DATABASE_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATABASE_DIR / "ibhotwe.db"
SECRET = os.getenv(
    "IBHOTWE_SECRET", "change-this-secret-in-production").encode()
COOKIE = "ibhotwe_session"

app = FastAPI(title="Ibhotwe Campus Food API", version="1.0.0")
app.mount("/css", StaticFiles(directory=FRONTEND_DIR / "css"), name="css")
app.mount("/js", StaticFiles(directory=FRONTEND_DIR / "js"), name="js")
app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.middleware("http")
async def no_cache_everything(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    return response

# ---------- Database ----------


def db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con


def hash_password(password: str, salt: bytes | None = None):
    salt = salt or secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200_000)
    return base64.b64encode(salt).decode() + "$" + base64.b64encode(digest).decode()


def verify_password(password, stored):
    try:
        salt_b64, digest_b64 = stored.split("$", 1)
        salt = base64.b64decode(salt_b64)
        expected = base64.b64decode(digest_b64)
        actual = hashlib.pbkdf2_hmac(
            "sha256", password.encode(), salt, 200_000)
        return hmac.compare_digest(actual, expected)
    except Exception:
        return False


def token_for(user_id: int):
    payload = {"uid": user_id, "exp": int(time.time()) + 60*60*24}
    raw = base64.urlsafe_b64encode(json.dumps(
        payload, separators=(",", ":")).encode()).decode().rstrip("=")
    sig = hmac.new(SECRET, raw.encode(), hashlib.sha256).hexdigest()
    return raw + "." + sig


def user_from_request(request: Request):
    token = request.cookies.get(COOKIE)
    if not token or "." not in token:
        return None
    raw, sig = token.rsplit(".", 1)
    good = hmac.compare_digest(sig, hmac.new(
        SECRET, raw.encode(), hashlib.sha256).hexdigest())
    if not good:
        return None
    try:
        payload = json.loads(base64.urlsafe_b64decode(
            raw + "=" * (-len(raw) % 4)))
        if payload["exp"] < time.time():
            return None
        con = db()
        user = con.execute("SELECT * FROM users WHERE id=?",
                           (payload["uid"],)).fetchone()
        con.close()
        return user
    except Exception:
        return None


def require_user(request: Request):
    user = user_from_request(request)
    if not user:
        raise HTTPException(401, "Please sign in first.")
    return user


def public_user(row):
    return {"id": row["id"], "name": row["name"], "email": row["email"], "campus": row["campus"],
            "student_number": row["student_number"], "loyalty_points": row["loyalty_points"], "role": row["role"]}


def init_db():
    con = db()
    con.executescript("""
    CREATE TABLE IF NOT EXISTS users(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL,
      student_number TEXT, campus TEXT NOT NULL, loyalty_points INTEGER NOT NULL DEFAULT 50,
      role TEXT NOT NULL DEFAULT 'student', created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS vendors(
      id TEXT PRIMARY KEY, name TEXT NOT NULL, campus TEXT NOT NULL, is_open INTEGER NOT NULL DEFAULT 1
    );
    CREATE TABLE IF NOT EXISTS products(
      id TEXT PRIMARY KEY, vendor_id TEXT NOT NULL, name TEXT NOT NULL, description TEXT,
      price REAL NOT NULL, category TEXT NOT NULL, image TEXT, rating REAL DEFAULT 4.5,
      reviews INTEGER DEFAULT 0, prep INTEGER DEFAULT 15, popular INTEGER DEFAULT 0,
      discount REAL DEFAULT 0, tags TEXT DEFAULT '[]',
      FOREIGN KEY(vendor_id) REFERENCES vendors(id)
    );
    CREATE TABLE IF NOT EXISTS orders(
      id TEXT PRIMARY KEY, user_id INTEGER NOT NULL, vendor_id TEXT NOT NULL,
      total REAL NOT NULL, status TEXT NOT NULL DEFAULT 'pending', payment TEXT NOT NULL,
      promo_code TEXT, placed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY(user_id) REFERENCES users(id), FOREIGN KEY(vendor_id) REFERENCES vendors(id)
    );
    CREATE TABLE IF NOT EXISTS order_items(
      id INTEGER PRIMARY KEY AUTOINCREMENT, order_id TEXT NOT NULL, product_id TEXT NOT NULL,
      name TEXT NOT NULL, price REAL NOT NULL, qty INTEGER NOT NULL,
      FOREIGN KEY(order_id) REFERENCES orders(id) ON DELETE CASCADE
    );
    """)
    vendors = [
        ("v1", "Mama's Kitchen", "Main Campus – Block C", 1),
        ("v2", "Campus Bites", "Student Union – Ground Floor", 1),
        ("v3", "The Green Bowl", "Science Block – Cafeteria", 1),
        ("v4", "Samoosa Palace", "Arts Block – Kiosk 7", 1),
        ("v5", "Slice & Dice", "Res Area – Common Room", 0)]
    con.executemany(
        "INSERT OR IGNORE INTO vendors(id,name,campus,is_open) VALUES(?,?,?,?)", vendors)
    imgs = {
        "stew": "https://images.unsplash.com/photo-1763048443535-1243379234e2?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=600",
        "burger": "https://images.unsplash.com/photo-1654987581885-a05493f5dc67?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=600",
        "wings": "https://images.unsplash.com/photo-1766589221522-d5beae155124?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=600",
        "bowl": "https://images.unsplash.com/photo-1644704170910-a0cdf183649b?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=600",
        "samosa": "https://images.unsplash.com/photo-1772729996007-40bad08b3c40?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=600",
        "pizza": "https://images.unsplash.com/photo-1688966601042-a7a794a2cdac?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=600",
        "smoothie": "https://images.unsplash.com/photo-1697642452436-9c40773cbcbb?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=600"}
    products = [
        ("f1", "v1", "Bunny Chow", "A hollowed-out loaf of white bread filled with spicy curry.",
         45, "traditional", "stew", 4.9, 204, 15, 1, 10, ["spicy", "filling", "veg-option"]),
        ("f2", "v1", "Pap & Wors", "Creamy maize pap served with flame-grilled boerewors and chakalaka.",
            55, "traditional", "stew", 4.7, 156, 20, 1, 0, ["hearty", "local-favourite"]),
        ("f3", "v1", "Boerewors Roll", "A juicy boerewors sausage in a fresh roll with tomato sauce and mustard.",
            35, "traditional", "stew", 4.6, 98, 10, 0, 0, ["quick", "budget-friendly"]),
        ("f4", "v2", "Classic Cheeseburger", "Juicy beef patty with cheddar, lettuce, tomato and secret sauce.",
            65, "fast-food", "burger", 4.5, 187, 12, 1, 15, ["students-favourite", "filling"]),
        ("f5", "v2", "Chicken Wings x6", "Crispy fried wings with peri-peri, BBQ or lemon herb sauce.",
            60, "fast-food", "wings", 4.7, 143, 18, 1, 0, ["shareable", "spicy-option"]),
        ("f6", "v2", "Gatsby Roll", "A massive sub loaded with chips, sausage, atchar and sauce.",
            70, "fast-food", "burger", 4.4, 89, 15, 0, 0, ["sharing", "huge"]),
        ("f7", "v3", "Avo Grain Bowl", "Quinoa and brown rice with avocado, roasted chickpeas and tahini.",
            75, "healthy", "bowl", 4.8, 112, 10, 1, 0, ["vegan", "gluten-free-option"]),
        ("f8", "v3", "Chicken Rice Bowl", "Grilled chicken over brown rice with roasted veggies and peri-peri.",
            70, "healthy", "bowl", 4.6, 95, 12, 0, 5, ["high-protein", "meal-prep"]),
        ("f9", "v4", "Samoosas x3", "Golden pastry triangles filled with spiced mince or vegetable curry.",
            25, "snacks", "samosa", 4.9, 278, 5, 1, 0, ["veg-option", "snack", "affordable"]),
        ("f10", "v4", "Spring Rolls x4", "Crispy vegetable spring rolls with sweet chilli sauce.",
            30, "snacks", "samosa", 4.5, 134, 8, 0, 0, ["vegan", "snack"]),
        ("f11", "v5", "Margarita Pizza", "Tomato base, fresh mozzarella and basil on a hand-tossed crust.",
            85, "pizza", "pizza", 4.4, 121, 25, 0, 20, ["vegetarian", "classic"]),
        ("f12", "v5", "Chicken Supreme Pizza", "Chicken, peppers, onions, mushrooms and cream sauce.",
            95, "pizza", "pizza", 4.6, 98, 30, 1, 0, ["group-meal", "hearty"]),
        ("f13", "v3", "Tropical Smoothie", "Mango, pineapple, banana and coconut water.",
            40, "drinks", "smoothie", 4.7, 167, 5, 1, 0, ["vegan", "refreshing", "cold"]),
        ("f14", "v3", "Green Detox Juice", "Spinach, cucumber, ginger, apple and lemon.", 45, "drinks", "smoothie", 4.5, 88, 5, 0, 0, ["detox", "healthy"])]
    for p in products:
        pid, vid, name, desc, price, cat, img, rating, reviews, prep, pop, discount, tags = p
        con.execute("""INSERT OR IGNORE INTO products
          (id,vendor_id,name,description,price,category,image,rating,reviews,prep,popular,discount,tags)
          VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (pid, vid, name, desc, price, cat, imgs[img], rating, reviews, prep, pop, discount, json.dumps(tags)))
    # Demo accounts
    demos = [
        ("Demo Student", "student@ibhotwe.co.za", "Student123!",
         "STU20240012", "Main Campus", 340, "student"),
        ("Thabo Mokoena", "thabo.mokoena@student.ac.za",
            "password123", "STU20240012", "Main Campus", 340, "student"),
        ("Demo Vendor", "vendor@ibhotwe.co.za",
            "Vendor123!", "VND001", "Main Campus", 0, "vendor"),
        ("Mama's Kitchen", "mama@kitchen.ac.za", "password123", "VND001", "Main Campus", 0, "vendor")]
    for name, email, pw, stnum, campus, pts, role in demos:
        if not con.execute("SELECT 1 FROM users WHERE email=?", (email,)).fetchone():
            con.execute("""INSERT INTO users(name,email,password_hash,student_number,campus,loyalty_points,role)
                           VALUES(?,?,?,?,?,?,?)""", (name, email, hash_password(pw), stnum, campus, pts, role))
    con.commit()
    con.close()


init_db()

# ---------- Schemas ----------


class Credentials(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    role: str | None = None


class RegisterIn(Credentials):
    name: str = Field(min_length=2)
    student_number: str = ""
    campus: str = "Main Campus"
    role: str = "student"


class OrderItemIn(BaseModel):
    product_id: str
    qty: int = Field(ge=1, le=50)


class OrderIn(BaseModel):
    items: list[OrderItemIn]
    payment: str = "mobile"
    promo_code: str | None = None


class MenuIn(BaseModel):
    name: str = Field(min_length=2)
    description: str = ""
    price: float = Field(gt=0)
    category: str = "traditional"
    prep: int = Field(default=15, ge=1, le=180)


class StatusIn(BaseModel):
    status: str

# ---------- Auth ----------


@app.post("/api/auth/register")
def register(data: RegisterIn, response: Response):
    con = db()
    role = "vendor" if (data.role or "").lower() == "vendor" else "student"
    try:
        cur = con.execute("""INSERT INTO users(name,email,password_hash,student_number,campus,loyalty_points,role)
                          VALUES(?,?,?,?,?,50,?)""",
                          (data.name, data.email.lower(), hash_password(data.password), data.student_number, data.campus, role))
        uid = cur.lastrowid
        con.commit()
        user = con.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()
    except sqlite3.IntegrityError:
        con.close()
        raise HTTPException(409, "An account with that email already exists.")
    con.close()
    response.set_cookie(COOKIE, token_for(uid), httponly=True,
                        samesite="lax", max_age=86400, path="/")
    return {"user": public_user(user)}


@app.post("/api/auth/login")
def login(data: Credentials, response: Response):
    con = db()
    user = con.execute("SELECT * FROM users WHERE email=?",
                       (data.email.lower(),)).fetchone()
    con.close()
    if not user or not verify_password(data.password, user["password_hash"]):
        raise HTTPException(401, "Incorrect email or password.")
    if data.role and data.role.lower() != user["role"].lower():
        expected = "Vendor" if user["role"] == "vendor" else "Student"
        chosen = "Vendor" if data.role.lower() == "vendor" else "Student"
        raise HTTPException(
            400, f"Role mismatch: This account is registered as a {expected}, but you selected {chosen}. Please confirm your role.")
    response.set_cookie(COOKIE, token_for(
        user["id"]), httponly=True, samesite="lax", max_age=86400, path="/")
    return {"user": public_user(user)}


@app.get("/api/auth/me")
def me(request: Request):
    user = require_user(request)
    return {"user": public_user(user)}


@app.post("/api/auth/logout")
def logout(response: Response):
    response.delete_cookie(COOKIE, path="/")
    return {"ok": True}

# ---------- Catalogue ----------


@app.get("/api/products")
def products():
    con = db()
    rows = con.execute("SELECT * FROM products").fetchall()
    con.close()
    return {"products": [dict(r) | {"tags": json.loads(r["tags"] or "[]"), "popular": bool(r["popular"])} for r in rows]}


@app.get("/api/vendors")
def vendors():
    con = db()
    rows = con.execute("SELECT * FROM vendors").fetchall()
    con.close()
    return {"vendors": [dict(r) | {"is_open": bool(r["is_open"])} for r in rows]}

# ---------- Orders ----------


def order_json(con, oid):
    o = con.execute(
        """SELECT o.*,v.name vendor_name FROM orders o JOIN vendors v ON v.id=o.vendor_id WHERE o.id=?""", (oid,)).fetchone()
    if not o:
        return None
    items = con.execute(
        "SELECT product_id,name,price,qty FROM order_items WHERE order_id=?", (oid,)).fetchall()
    return {"id": o["id"], "items": [dict(i) for i in items], "total": round(o["total"], 2), "status": o["status"],
            "vendorName": o["vendor_name"], "placedAt": o["placed_at"], "est": "20 mins" if o["status"] != "completed" else "Done",
            "payment": o["payment"], "promo_code": o["promo_code"]}


@app.get("/api/orders")
def get_orders(request: Request):
    user = require_user(request)
    if user["role"] != "student":
        raise HTTPException(
            403, "Vendor accounts do not have a student order history.")
    con = db()
    ids = con.execute(
        "SELECT id FROM orders WHERE user_id=? ORDER BY placed_at DESC", (user["id"],)).fetchall()
    result = [order_json(con, r["id"]) for r in ids]
    con.close()
    return {"orders": result}


@app.post("/api/orders")
def create_order(data: OrderIn, request: Request):
    user = require_user(request)
    if user["role"] != "student":
        raise HTTPException(403, "Vendor accounts cannot place orders.")
    if not data.items:
        raise HTTPException(400, "Your cart is empty.")
    con = db()
    total = 0
    chosen = []
    vendor_ids = set()
    for item in data.items:
        p = con.execute("SELECT * FROM products WHERE id=?",
                        (item.product_id,)).fetchone()
        if not p:
            con.close()
            raise HTTPException(
                404, f"Product {item.product_id} was not found.")
        price = p["price"]*(1-(p["discount"] or 0)/100)
        total += price*item.qty
        chosen.append((p, item, price))
        vendor_ids.add(p["vendor_id"])
    if len(vendor_ids) > 1:
        con.close()
        raise HTTPException(
            400, "For this MVP, all cart items must come from one vendor.")
    if data.promo_code:
        codes = {"MONDAY20": 20, "EXAMTIME": 50, "WELCOME15": 15}
        discount = codes.get(data.promo_code.upper())
        if discount:
            total *= (1-discount/100)
    oid = "ORD-"+secrets.token_hex(3).upper()
    vid = next(iter(vendor_ids))
    con.execute("INSERT INTO orders(id,user_id,vendor_id,total,status,payment,promo_code) VALUES(?,?,?,?,?,?,?)",
                (oid, user["id"], vid, round(total, 2), "pending", data.payment, data.promo_code))
    for p, item, price in chosen:
        con.execute("INSERT INTO order_items(order_id,product_id,name,price,qty) VALUES(?,?,?,?,?)",
                    (oid, p["id"], p["name"], price, item.qty))
    con.execute(
        "UPDATE users SET loyalty_points=loyalty_points+10 WHERE id=?", (user["id"],))
    con.commit()
    result = order_json(con, oid)
    con.close()
    return {"order": result}

# ---------- Vendor ----------


@app.get("/api/vendor")
def vendor(request: Request):
    user = require_user(request)
    if user["role"] != "vendor":
        raise HTTPException(403, "Vendor account required.")
    con = db()
    v = con.execute("SELECT * FROM vendors WHERE id='v1'").fetchone()
    con.close()
    return {"vendor": dict(v) | {"is_open": bool(v["is_open"])}}


@app.get("/api/vendor/orders")
def vendor_orders(request: Request):
    user = require_user(request)
    if user["role"] != "vendor":
        raise HTTPException(403, "Vendor account required.")
    con = db()
    ids = con.execute(
        "SELECT id FROM orders WHERE vendor_id='v1' ORDER BY placed_at DESC").fetchall()
    result = [order_json(con, r["id"]) for r in ids]
    con.close()
    return {"orders": result}


@app.get("/api/vendor/menu")
def vendor_menu(request: Request):
    user = require_user(request)
    if user["role"] != "vendor":
        raise HTTPException(403, "Vendor account required.")
    con = db()
    rows = con.execute(
        "SELECT * FROM products WHERE vendor_id='v1' ORDER BY name").fetchall()
    con.close()
    return {"items": [dict(r) | {"tags": json.loads(r["tags"] or "[]"), "popular": bool(r["popular"])} for r in rows]}


@app.post("/api/vendor/menu")
def add_menu(data: MenuIn, request: Request):
    user = require_user(request)
    if user["role"] != "vendor":
        raise HTTPException(403, "Vendor account required.")
    con = db()
    pid = "f"+secrets.token_hex(4)
    con.execute("""INSERT INTO products(id,vendor_id,name,description,price,category,image,rating,reviews,prep,popular,discount,tags)
                   VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (pid, "v1", data.name, data.description, data.price, data.category,
                 "https://images.unsplash.com/photo-1763048443535-1243379234e2?fit=crop&w=600",
                 4.5, 0, data.prep, 0, 0, "[]"))
    con.commit()
    row = con.execute("SELECT * FROM products WHERE id=?", (pid,)).fetchone()
    con.close()
    return {"item": dict(row) | {"tags": [], "popular": False}}


@app.delete("/api/vendor/menu/{product_id}")
def delete_menu(product_id: str, request: Request):
    user = require_user(request)
    if user["role"] != "vendor":
        raise HTTPException(403, "Vendor account required.")
    con = db()
    cur = con.execute(
        "DELETE FROM products WHERE id=? AND vendor_id='v1'", (product_id,))
    con.commit()
    con.close()
    if cur.rowcount == 0:
        raise HTTPException(404, "Menu item not found.")
    return {"ok": True}


@app.patch("/api/vendor/orders/{oid}")
def update_order(oid: str, data: StatusIn, request: Request):
    user = require_user(request)
    if user["role"] != "vendor":
        raise HTTPException(403, "Vendor account required.")
    if data.status not in {"pending", "preparing", "ready", "completed", "cancelled"}:
        raise HTTPException(400, "Invalid order status.")
    con = db()
    cur = con.execute(
        "UPDATE orders SET status=? WHERE id=? AND vendor_id='v1'", (data.status, oid))
    con.commit()
    if cur.rowcount == 0:
        con.close()
        raise HTTPException(404, "Order not found.")
    result = order_json(con, oid)
    con.close()
    return {"order": result}

# ---------- Pages ----------


@app.get("/")
def root():
    resp = FileResponse(FRONTEND_DIR / "login.html")
    resp.delete_cookie(COOKIE, path="/")
    return resp


@app.get("/login.html")
def login_page():
    resp = FileResponse(FRONTEND_DIR / "login.html")
    resp.delete_cookie(COOKIE, path="/")
    return resp


@app.get("/{page}.html")
def page(page: str, request: Request):
    allowed = {"home", "browse", "cart", "orders", "vendor", "game", "login"}
    if page not in allowed:
        raise HTTPException(404, "Page not found")
    user = user_from_request(request)
    if not user:
        return Response(status_code=303, headers={"Location": "/login.html"})
    if page == "vendor" and user["role"] != "vendor":
        return Response(status_code=303, headers={"Location": "/home.html"})
    if page != "vendor" and user["role"] == "vendor":
        return Response(status_code=303, headers={"Location": "/vendor.html"})
    return FileResponse(FRONTEND_DIR / f"{page}.html")
