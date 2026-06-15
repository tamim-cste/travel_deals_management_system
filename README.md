# Travel Deal Management System

A modular REST API built with Flask and SQLite to manage, search, filter, and sort travel deals.

---

## What This Project Does

- Add a new travel deal
- View all deals
- View a single deal
- Search deals by destination, platform, or travel type
- Filter deals by price range
- Sort deals by any field
- Track recently viewed deals
- Log all API activities

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3 | Programming language |
| Flask | Web framework |
| Flask-SQLAlchemy | ORM for database |
| SQLite | Lightweight database |
| logging | Activity tracking |

---

## Project Structure

```
project/
├── app.py                    # App entry point & config
├── routes/
│   └── deal_routes.py        # All API endpoints
├── services/
│   └── deal_service.py       # Business logic
├── utils/
│   ├── validators.py         # Reusable input validation
│   └── logger.py             # Logging setup
├── database/
│   └── store.py              # DB models & queries
├── logs/
│   └── app.log               # Generated at runtime
├── requirements.txt
└── README.md
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/tamim-cste/travel_deals_management_system
cd travel_deals_management_system
```

### 2. Create and activate virtual environment

```bash
python3 -m venv venv

# Mac/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip3 install -r requirements.txt
```

### 4. Run the server

```bash
python3 app.py
```

API will be running at: `http://127.0.0.1:5000`

> A `logs/app.log` file and `instance/travel_deals.db` database will be created automatically on first run.

---

## API Reference

### 1. Add a Travel Deal
```
POST /deals
```
**Request Body:**
```json
{
  "destination": "Dubai",
  "price": 5000,
  "platform": "Booking",
  "rating": 4.5,
  "travel_type": "Luxury"
}
```
**Success → 201** | **Validation Error → 422**

---

### 2. Get All Deals
```
GET /deals
```
**Success → 200**

---

### 3. Get Single Deal
```
GET /deals/<deal_id>
```
**Success → 200** | **Not Found → 404**

---

### 4. Search Deals
```
GET /deals/search?destination=dubai
GET /deals/search?platform=booking
GET /deals/search?travel_type=Luxury
GET /deals/search?destination=dubai&platform=booking
```
- Case-insensitive
- Partial match supported
- At least one parameter required

**Success → 200** | **No params → 400**

---

### 5. Filter by Price Range
```
GET /deals/filter?min_price=1000&max_price=5000
GET /deals/filter?min_price=2000
GET /deals/filter?max_price=3000
```
**Success → 200** | **Validation Error → 422**

---

### 6. Sort Deals
```
GET /deals/sort?sort_by=price&order=asc
GET /deals/sort?sort_by=rating&order=desc
```
**Allowed sort_by values:** `price`, `rating`, `destination`, `created_at`

**Allowed order values:** `asc`, `desc`

**Success → 200** | **Invalid field/order → 422**

---

### 7. Recently Viewed Deals
```
GET /deals/recent
```
Tracks the last 10 individually viewed deals (via `GET /deals/<id>`).

**Success → 200**

---

## Validation Rules

### Deal Creation
| Field | Rule |
|---|---|
| `destination` | Required, non-empty string |
| `price` | Required, positive number |
| `platform` | Required, non-empty string |
| `rating` | Required, number between 1–5 |
| `travel_type` | Must be: `Budget`, `Luxury`, `Adventure`, `Family` |

### Filter
| Param | Rule |
|---|---|
| `min_price` | Cannot be negative |
| `max_price` | Cannot be negative or less than `min_price` |

### Sort
| Param | Rule |
|---|---|
| `sort_by` | Must be one of: `price`, `rating`, `destination`, `created_at` |
| `order` | Must be `asc` or `desc` |

---

## HTTP Status Codes

| Code | Meaning |
|---|---|
| `200` | OK |
| `201` | Created |
| `400` | Bad Request |
| `404` | Not Found |
| `422` | Validation Failed |
| `500` | Internal Server Error |

---

## Logging

All API activity is logged to `logs/app.log` and printed to the terminal.

| Level | When used |
|---|---|
| `INFO` | Successful operations |
| `WARNING` | Validation errors, empty searches |
| `ERROR` | Missing request body, resource not found |
