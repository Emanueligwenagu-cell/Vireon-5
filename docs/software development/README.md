# Ibhotwe – Campus Food Ordering Platform

Django + Django REST Framework backend, MySQL database, and a static
frontend, for the WSU Ibhotwe cafeteria ordering group project.

## Project layout

```
Ibotwe_FoodOrdering_System/
├── backend/        Django/DRF API (accounts, vendors, menu, orders, payments, promos, game)
├── frontend/        Existing static site, now wired up to the API via js/api.js + js/auth.js
└── README.md
```

## Backend setup

```bash
cd backend
python -m venv venv
source venv/bin/activate          # macOS/Linux
# Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Copy the environment template and edit the new local file. Never commit or
share `.env`:

```text
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

You'll need a MySQL database and user matching what you put in `.env`:

```sql
CREATE DATABASE ibotwe CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'ibotwe_user'@'localhost' IDENTIFIED BY 'replace-with-a-strong-password';
GRANT ALL PRIVILEGES ON ibotwe.* TO 'ibotwe_user'@'localhost';
FLUSH PRIVILEGES;
```

Then:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The API is now at `http://127.0.0.1:8000/api/`, and Django admin at
`http://127.0.0.1:8000/admin/`.

## Frontend setup

The frontend is static. Serve `frontend/` with VS Code Live Server or run:

```bash
cd frontend
python -m http.server 5500
```

Open `http://127.0.0.1:5500`. The frontend API base URL is configured in
`frontend/index.html` and defaults to `http://127.0.0.1:8000/api`.

## Accounts: password or Google

Both are supported:
- **Email + password**: `POST /api/auth/register/`, then `POST /api/auth/login/`.
  Passwords are hashed (never stored in plain text) and validated against
  Django's strength rules (10+ chars, not a common password, not all-numeric).
- **Google**: the frontend uses Google Identity Services
  (`js/auth.js` → `initGoogleSignIn(clientId, buttonElementId)`) to get an
  ID token, then sends it to `POST /api/auth/google/`, which verifies it
  directly with Google's servers before creating/logging in the account.
  You'll need to create an OAuth 2.0 Client ID in the
  [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
  and put it in both `backend/.env` (`GOOGLE_OAUTH_CLIENT_ID`) and the
  frontend call to `initGoogleSignIn`.

Both paths return the same JWT access/refresh token pair, so the rest of
the app doesn't need to know how someone signed in.

## Security measures built in

- **Password hashing** via Django's PBKDF2 hasher; raw passwords are never stored.
- **JWT auth** (short-lived access tokens + rotating, blacklist-on-logout refresh tokens).
- **Server-side money calculations**: order totals, discounts, and payment
  amounts are always computed from the database (current menu prices,
  promo rules), never trusted from the client — see the tests in
  `orders/tests.py` and `payments/tests.py` for what this protects against.
- **Role-based permissions** (student / vendor / admin) enforced per-endpoint
  and per-object (a vendor can only edit their own stall/menu; a student can
  only see their own orders).
- **Rate limiting** on auth endpoints (register/login/Google) to slow down
  credential-stuffing and brute-force attempts.
- **CORS locked down** to only the frontend origin(s) listed in `.env`.
- **Secrets kept out of source control** via `.env` (gitignored); `.env.example`
  documents what's needed without containing real values.
- **Production hardening** (HTTPS redirect, HSTS, secure cookies) auto-enabled
  whenever `DEBUG=False`.
- Django's ORM parameterizes all queries, so standard SQL injection via the
  API isn't possible as long as you keep using the ORM (avoid raw SQL).

## Not yet wired up (needs your input)

- **Real payment gateway**: `payments/services.py` has a pluggable
  `PaymentGateway` interface. Cash-on-pickup works locally, while electronic
  payments are disabled when `DEBUG=False` until a real provider with webhook
  verification and idempotency protection is integrated.
- **Deployment**: settings are environment-driven and `gunicorn`/`whitenoise`
  are in `requirements.txt`, but hosting (server, HTTPS certificate, domain)
  is up to your team to set up.
