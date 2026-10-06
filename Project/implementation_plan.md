# Implementation Plan — Ibhotwe Campus Food Ordering Platform (Walter Sisulu University)

Develop and integrate a Python **FastAPI** backend with a **MySQL** database for the **Ibhotwe (Walter Sisulu University - WSU)** campus food ordering platform, connecting all features of the existing HTML/CSS/JavaScript frontend.

---

## User Review Required

> [!IMPORTANT]
> **Institution & Branding**: Configured specifically for **Walter Sisulu University (WSU)** students and campus cafeteria vendors across campus sites (Main Campus, Science & Engineering, Medical Campus, Arts & Design, Off-Campus Residences).

> [!NOTE]
> **Database Credentials & Environment**: The backend will use SQLAlchemy with PyMySQL. A `.env.example` file will be provided with default settings (`mysql+pymysql://root:password@localhost:3306/ibhotwe_db`). You will just need your local MySQL server running or use SQLite during initial local testing if MySQL is not yet configured.

> [!NOTE]
> **Starter Seed Data**: The database initialization script (`schema.sql` / seed utility) will be automatically populated with your exact campus vendors (*Mama's Kitchen*, *Campus Bites*, *The Green Bowl*, *Samoosa Palace*, *Slice & Dice*), menu items (*Bunny Chow*, *Pap & Wors*, *Gatsby Roll*, etc.), and promo codes (*MONDAY20*, *EXAMTIME*, *WELCOME15*).

---

## Proposed System Architecture

```
                                 ┌─────────────────────────────────────────┐
                                 │ Frontend (HTML5 / CSS3 / Vanilla JS)    │
                                 │  • Walter Sisulu University UI          │
                                 │  • js/api.js (fetch client + JWT)       │
                                 │  • js/pages/* (Home, Browse, Cart, etc.)│
                                 └───────────────────▲─────────────────────┘
                                                     │ JSON REST API
                                                     ▼
                                 ┌─────────────────────────────────────────┐
                                 │ FastAPI Application (main.py)           │
                                 │  • CORS Middleware                      │
                                 │  • Pydantic v2 Request/Response Schemas │
                                 │  • OAuth2 / JWT Bearer Auth Guards      │
                                 │  • Modular Routers (/api/...)           │
                                 └───────────────────▲─────────────────────┘
                                                     │ SQLAlchemy 2.0 ORM
                                                     ▼
                                 ┌─────────────────────────────────────────┐
                                 │ MySQL Database (ibhotwe_db)             │
                                 │  • users, vendors, categories           │
                                 │  • menu_items, orders, order_items      │
                                 │  • promo_codes                          │
                                 └─────────────────────────────────────────┘
```

---

## Proposed Changes & Code Structure

The project will be organized in `C:\Users\ACER.NTS\.gemini\antigravity\scratch\wsu-ibhotwe-food-ordering`:

### 1. Database & Core Infrastructure (`backend/app/core/`)
- [NEW] `backend/app/core/config.py`: Application settings (Database URL, JWT Secret Key, Token Expiry, CORS Origins).
- [NEW] `backend/app/core/database.py`: SQLAlchemy engine, `SessionLocal`, base declarative model class, and `get_db()` dependency.
- [NEW] `backend/app/core/security.py`: Password hashing using Bcrypt, JWT token creation, and current user retrieval dependency (`get_current_user`, `require_role`).

### 2. Database Models (`backend/app/models/`)
- [NEW] `backend/app/models/user.py`: `User` table (ID, WSU student/staff number, full name, email, hashed password, role, campus, loyalty points).
- [NEW] `backend/app/models/vendor.py`: `Vendor` table (ID, owner ID, name, campus location, image URL, is_open, rating, reviews count, min_order).
- [NEW] `backend/app/models/menu.py`: `Category` and `MenuItem` tables (category, name, description, price, prep time, image, is_available, rating, tags).
- [NEW] `backend/app/models/order.py`: `Order` and `OrderItem` tables (order code, fulfillment type, delivery location, status, total, payment method, timestamps).
- [NEW] `backend/app/models/promo.py`: `PromoCode` table (code, discount percentage, active state).

### 3. Pydantic Schemas (`backend/app/schemas/`)
- [NEW] `backend/app/schemas/auth.py`: `UserRegister`, `UserLogin`, `UserOut`, `TokenResponse`.
- [NEW] `backend/app/schemas/menu.py`: `MenuItemCreate`, `MenuItemUpdate`, `MenuItemOut`, `CategoryOut`.
- [NEW] `backend/app/schemas/vendor.py`: `VendorOut`, `VendorStatusUpdate`, `VendorStatsOut`.
- [NEW] `backend/app/schemas/order.py`: `OrderCreate`, `OrderItemCreate`, `OrderOut`, `OrderStatusUpdate`.
- [NEW] `backend/app/schemas/promo.py`: `PromoValidateRequest`, `PromoValidateResponse`.

### 4. API Endpoints / Routers (`backend/app/routes/`)
- [NEW] `backend/app/routes/auth.py`:
  - `POST /api/auth/register` (Registers WSU user, awards 50 starter loyalty points, returns JWT).
  - `POST /api/auth/login` (Authenticates user, returns JWT and user profile).
  - `GET /api/auth/me` (Returns current user's profile and loyalty balance).
- [NEW] `backend/app/routes/vendors.py`:
  - `GET /api/vendors` (Lists all campus vendors with open/closed status).
  - `GET /api/vendors/{id}` (Vendor profile and details).
- [NEW] `backend/app/routes/menu.py`:
  - `GET /api/categories` (Returns list of food categories).
  - `GET /api/menu-items` (Search, category filter, max price, min rating, sorting).
- [NEW] `backend/app/routes/orders.py`:
  - `POST /api/orders` (Validates cart items, applies promo code, creates order, awards +10 loyalty points).
  - `GET /api/orders/my-orders` (Returns student's active and past orders).
  - `POST /api/orders/{id}/rate` (Allows student to submit a 1-5 star rating).
- [NEW] `backend/app/routes/vendor_admin.py`:
  - `GET /api/vendor/stats` (Revenue, active order counts, completed orders, popular items).
  - `GET /api/vendor/orders` (Live incoming orders queue).
  - `PATCH /api/vendor/orders/{id}/status` (Updates status: pending → preparing → ready → completed).
  - `POST /api/vendor/menu-items` (Adds new dish from Add Item modal).
  - `DELETE /api/vendor/menu-items/{id}` (Removes dish).
  - `PATCH /api/vendor/status` (Toggles Open/Closed state).
- [NEW] `backend/app/routes/promos.py`:
  - `POST /api/promos/validate` (Validates MONDAY20, EXAMTIME, WELCOME15).
- [NEW] `backend/app/routes/game.py`:
  - `POST /api/game/reward` (Awards bonus loyalty points when students play Tic-Tac-Toe).

### 5. Application Entrypoint & Database Seeder
- [NEW] `backend/app/main.py`: Creates FastAPI instance, configures CORS, registers all routers, and automatically creates tables on startup.
- [NEW] `backend/schema.sql`: Full DDL script with initial seed data.
- [NEW] `backend/seed.py`: Standalone Python script to seed initial vendors and meals.
- [NEW] `backend/requirements.txt`: Python dependencies.
- [NEW] `backend/.env.example`: Environment variables template.

### 6. Frontend API Integration Layer
- [NEW] `frontend/js/api.js`: Unified API client connecting UI forms and buttons to FastAPI endpoints.
- [NEW] Fully consolidated frontend files (`index.html`, `css/styles.css`, `js/data.js`, `js/state.js`, `js/utils.js`, `js/components.js`, `js/router.js`, `js/nav.js`, `js/main.js`, and all `js/pages/*.js`).

### 7. Version Control & Documentation
- [NEW] `.gitignore`: Excludes Python virtual environment, cache, local databases, and secrets.
- [NEW] `README.md`: Complete guide on how to setup MySQL, run FastAPI with Uvicorn, test with Swagger UI (`http://127.0.0.1:8000/docs`), and manage GitHub feature branches.

---

## Verification Plan

### Automated & Manual Verification
1. **API Docs Verification**: Start the FastAPI server using `uvicorn app.main:app --reload` and verify all endpoints via interactive Swagger UI at `http://127.0.0.1:8000/docs`.
2. **Database Seeding**: Run `python seed.py` and check that all 5 vendors, 14 food items, categories, and promo codes are inserted.
3. **Authentication Flow**: Test user registration, token generation, login, and token-based route protection.
4. **Order Lifecycle Flow**:
   - Place an order through the frontend Cart.
   - Verify order appears in "My Orders" as `pending`.
   - Verify order appears in Vendor Portal queue.
   - Transition status (`pending` → `preparing` → `ready` → `completed`) and verify real-time UI updates.
5. **Vendor Management**: Add a new item via the Add Item modal and confirm it appears in the Browse catalog and database.
