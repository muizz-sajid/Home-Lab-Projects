# Finance Web Application

A dynamic web application built with Flask and SQLite that simulates a stock trading platform. This project is a customized version of the CS50x Finance problem set, extended with aesthetic enhancements (custom CSS and animations) and a new feature: the ability to add virtual cash to your account.

---

## Table of Contents

1. [Overview](#overview)  
2. [Features](#features)  
3. [Project Structure](#project-structure)  
4. [Screenshots](#screenshots)  
5. [Setup & Installation](#setup--installation)  
6. [Database Schema](#database-schema)  
7. [Custom Styling](#custom-styling)  
8. [Technologies Used](#technologies-used)  
9. [Known Limitations](#known-limitations)    
10. [Acknowledgments](#acknowledgments) 

---

## Overview

This web app allows users to register, log in, and simulate the process of buying and selling stocks using real‑time data fetched from the CS50 Finance API wrapper. It keeps track of user portfolios and provides a complete transaction history. Additionally, users can **add virtual cash** to their account for experimentation.

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

## Setup & Installation

### Prerequisites

- Python 3.10+
- `pip` package manager
- SQLite (included with Python)

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/finance
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

