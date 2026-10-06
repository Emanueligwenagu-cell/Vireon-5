# Ibhotwe Campus Food Ordering Platform (WSU)

A full-stack campus food ordering platform built for Walter Sisulu University (WSU) students and food vendors.

## Key Features

- **Multi-page Architecture**: Real HTML pages (`/login.html`, `/home.html`, `/browse.html`, `/cart.html`, `/orders.html`, `/vendor.html`, `/game.html`) with browser back/forward navigation support.
- **Strict Role-Based Access Control**:
  - **Logged-out by default**: When opening the platform (`/`), previous sessions are cleared, requiring users to log in.
  - **Login Role Confirmation**: The login screen asks whether the user is signing in as a **Student** or a **Vendor** and verifies the account type before granting access.
  - **Vendor-only Access**: The `/vendor.html` page and all `/api/vendor/*` endpoints can only be accessed if and only if a vendor is logged in. Unauthorized visits or student attempts redirect immediately to `/home.html`.
  - **Role-based Navigation**: Students see food browsing, cart, orders, and games. Vendors only see the vendor dashboard and incoming orders.
- **Order Management & Tracking**: Real-time order placement, status tracking (pending, preparing, ready, completed), and vendor kitchen dashboard.
- **Campus Loyalty Program**: Students earn 10 loyalty points per order and 50 points on registration.
- **Interactive Tic-Tac-Toe Game**: Play games while waiting for food to be prepared.

---

## Quick Start (How to Run)

### Windows
Double-click `start.bat`, or run from terminal:
```powershell
py -m uvicorn main:app --reload
```
*(You can also run directly from the `backend/` folder: `py -m uvicorn backend.main:app --reload`)*

### macOS / Linux
```bash
chmod +x start.sh
./start.sh
```

Then open your browser at:
👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## Demo Accounts

| Role | Email | Password | Access / Destination |
| :--- | :--- | :--- | :--- |
| **🎒 Student** | `student@ibhotwe.co.za` *(or `thabo.mokoena@student.ac.za`)* | `Student123!` *(or `password123`)* | Redirects to `/home.html` (Student food ordering) |
| **👨‍🍳 Vendor** | `vendor@ibhotwe.co.za` *(or `mama@kitchen.ac.za`)* | `Vendor123!` *(or `password123`)* | Redirects to `/vendor.html` (Vendor Kitchen Dashboard) |

*(Quick-fill demo buttons are also provided directly on the login page for instant testing).*

---

## Project Structure

The project is cleanly separated into **frontend**, **backend**, and **database** folders:

```text
wsu-ibhotwe-food-ordering/
├── backend/                                     # Server & REST API
│   ├── main.py                                  # FastAPI app, authentication & business logic
│   ├── requirements.txt                         # Python dependencies
│   └── README.md                                # Backend documentation
│
├── database/                                    # Database storage
│   ├── ibhotwe.db                               # SQLite database (auto-created if missing)
│   └── README.md                                # Database schema & tables guide
│
├── frontend/                                    # User Interface & client code
│   ├── login.html                               # Login & Registration page (role selector)
│   ├── home.html                                # Student home page
│   ├── browse.html                              # Food catalogue and filters
│   ├── cart.html                                # Cart checkout & promo codes
│   ├── orders.html                              # Order tracking & history
│   ├── vendor.html                              # Vendor kitchen dashboard
│   ├── game.html                                # Tic-Tac-Toe game
│   ├── css/
│   │   └── styles.css                           # Application styling
│   └── js/
│       ├── app.js                               # Page loader & role enforcement
│       ├── data.js                              # Initial catalogue & vendor data
│       ├── state.js                             # Reactive application state
│       ├── utils.js                             # Helper functions & formatters
│       ├── components.js                        # Reusable UI components
│       ├── nav.js                               # Header navigation, mobile menu & logout
│       └── pages/
│           ├── login.js                         # Role confirmation & auth logic
│           ├── home.js                          # Home page view
│           ├── browse.js                        # Browse catalog view
│           ├── cart.js                          # Cart view
│           ├── orders.js                        # Orders tracking view
│           ├── vendor.js                        # Vendor dashboard view
│           └── game.js                          # Gamification view
│
├── main.py                                      # Root entrypoint forwarder
├── start.bat                                    # Windows quick start script
├── start.sh                                     # Linux/Mac quick start script
├── CSS37W2_Class_Progress_Report_07_Sept.pdf    # Academic project report
└── README.md                                    # Project documentation
```
