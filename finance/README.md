# Stock-Trading Web Application

This dynamic stock trading platform lets users register, log in, and simulate buying and selling stocks using real‑time market data from a public API. It tracks user portfolios, maintains a full transaction history, and includes an “add virtual cash” feature for experimentation. Even though this web app contains a css file to enhance its visual presentation, the main idea is to showcase the backend workings of how each webpage, that are all designed with different purposes, works with each other and how the data for each user (that registered) is stored seperately in the sql database along with their encrypted password.

---

## Table of Contents

1. [Overview](#overview)  
2. [Features](#features)  
3. [Project Structure](#project-structure)  
4. [Screenshots](#screenshots) 
5. [Flow](#high-level-architecture-flow-of-requests) 
6. [Security & Privacy](#security--privacy)
7. [Database Schema](#database-schema)
8. [Setup & Installation](#setup--installation)
9. [Custom Styling](#custom-styling)  
10. [Technologies Used](#technologies-used)  
11. [Known Limitations](#known-limitations)    
12. [Acknowledgments](#acknowledgments) 

---

## Overview

This web app is built with Flask and SQLite which simulates a full-featured stock trading platform. It’s been enhanced with custom CSS, smooth animations to make the experience of buying, selling, quoting, viewing, logging in and registring with a new account seamless.

---

## Features

- **User Authentication**  
  Secure registration and login using hashed passwords.  
- **Stock Quote Lookup**  
  Fetches real‑time stock data via CS50’s API endpoint.  
- **Buy & Sell Stocks**  
  Transactions validated server‑side to prevent invalid orders.  
- **Portfolio Overview**  
  Displays current holdings with market values.  
- **Transaction History**  
  Logs each buy/sell with timestamps.  
- **Add Cash**  
  Inject additional virtual currency into your account.  
- **Apology Handling**  
  Custom error messages rendered as meme‑style images.  
- **Animated UI**  
  Integrated AOS (Animate On Scroll) for engaging interface effects.

---

## Project Structure

```bash
finance/
├── app.py                # Main application logic and route handling
├── finance.db            # SQLite3 database file (not shared here)
├── helpers.py            # Custom functions: API lookup, login_required, apology, USD formatting
├── requirements.txt      # Python package dependencies
│
├── static/
│   ├── favicon.ico       # Site icon
│   └── styles.css        # Fully customized dark theme with Poppins font and gradient buttons
│
├── templates/
│   ├── layout.html       # Base layout using Bootstrap 5 + AOS animations
│   ├── *.html            # Pages: buy, sell, login, register, quote, history, index, etc.
│
├── flask_session/        # Server‑side session files
└── __pycache__/          # Compiled bytecode (ignored)
```

## Screenshots

Add screenshots or GIFs here if deploying publicly (e.g., login screen, dashboard, buy/sell modals)


## High-Level Architecture (Flow of Requests)

Requests in this application flow through the following steps:

1. **Client ↔ Browser:** The user sends requests with the U.I in their browser.

2. **Flask Routes:** Every time a user clicks “buy”, ask for a quote, or check their history, Flask routes your request to the matching handler in app.py—like /buy, /quote, or /history.

3. **Authentication & Validation:** Decorators (for e.g. @login_required) and form validation gurantee only authorized requests proceed.

4. **Business Logic & Helpers:** Core operations—stock lookups (`helpers.lookup`), USD formatting (`helpers.usd`), and database updates—are handled by helper functions and route handlers.

5. **Database Operations:** Interactions with `finance.db` via SQL library record user credentials (`users` table) and transactions (`tracking` table).

6. **Template Rendering:** Information is sent to Jinja2 templates placed in the templates/ directory, mixing the base structure (layout.html) with dynamic content.

7. **Client Response:** The browser receives a responsive HTML file with static assets including CSS, Javascript, and favicon.


## Security & Privacy

**Password Storage:** The method used for hashing is Werkzeug’s generate_password_hash and check_password_hash, whereby a user’s password will never be stored in the system unencrypted.

**Session Management:** Uses server-side sessions (with flask-session) to avoid client-side tampering by storing session data on the server instead of using cookies.

**Input Sanitization:** All user input is checked and sanitized. Only valid stock symbols and share quantities in integer form are accepted to reduce injection attempts.

**HTTPS Recommendation:** For production deployments, it is strongly recommended that HTTPS should be enabled with TLS certificates to protect data transiting the network.

**API Key Handling:** No direct API keys are present as lookups are done externally through the CS50 Finance proxy endpoint which limits key exposure.


## Database Schema

The app uses a SQLite database (finance.db) with the following tables:

### `users`

| Column   | Type    | Description            |
|:---------|:--------|:------------------------|
| id       | INTEGER | Primary key             |
| username | TEXT    | Unique login name       |
| hash     | TEXT    | Hashed password         |
| cash     | REAL    | User's current balance  |

### `tracking`

| Column         | Type    | Description                            |
|:---------------|:--------|:----------------------------------------|
| id             | INTEGER | Primary key                            |
| user_id        | INTEGER | Foreign key to `users`                 |
| symbol         | TEXT    | Stock ticker symbol                    |
| shares         | INTEGER | Positive for buy, negative for sell    |
| price          | REAL    | Price per share at time of transaction |
| purchase_time  | TEXT    | Timestamp of transaction               |

> All transactions (buys/sells) are recorded in the tracking table with timestamp.


## Setup & Installation

### Prerequisites

- Python 3.10+
- `pip` package manager
- SQLite (included with Python)

### 1. Clone Repository

```bash
git clone https://github.com/muizz-sajid/Home-Lab-Projects/tree/main/finance
cd finance
```

### 2. Create Virtual Environment (Optional)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
```
(Windows CMD)

```cmd
set FLASK_APP=app.py
set FLASK_ENV=development
```

### 5. Run Flask Server

flask run

Visit http://127.0.0.1:5000 in your browser.


## Custom Styling

The static/styles.css file includes:

- Dark mode UI with color variables and gradients

- Google Fonts integration (Poppins)

- Custom navbar with text glow and hover effects

- Stylized buttons and tables with animation support

- Accessibility: Text contrast and hover cues

Animations powered by AOS (Animate On Scroll) using:

```html
<link href="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.js"></script>
```

## Technologies Used

- Python 3

- Flask

- SQLite3

- Jinja2 Templates

- HTML5/CSS3

- Bootstrap 5.3

- AOS (Animate On Scroll)

- Requests (HTTP library)

- Werkzeug (security)

- CS50 Finance API (lookup)


## Known Limitations

- Real-time data source is limited to CS50-provided API proxy (no direct IEX API key used)

- Database is SQLite; for production, a more robust DB (PostgreSQL, MySQL) would be preferred

- No stock quantity validation beyond integer input (decimal shares not supported)

- Session timeout and persistent logins are basic (flask-session only)


## Acknowledgments
- [Harvard CS50x](https://cs50.harvard.edu/x/)
- [AOS.js](https://michalsnik.github.io/aos/)
- [Bootstrap 5](https://getbootstrap.com/)
- [IEX Cloud](https://iexcloud.io/)
- [Memegen](https://memegen.link/) — for apology meme response

- Custom CSS theme and interface enhancements by the creator of the program

