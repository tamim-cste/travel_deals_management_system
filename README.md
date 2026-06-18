# Travel Deal Management System

A modular REST API built with Flask and SQLite to manage, search, filter, sort, and track travel deals — including update/delete operations, popularity tracking, and API usage statistics.

---

## What This Project Does

- Add a new travel deal
- View all deals
- View a single deal
- Update an existing deal
- Delete a deal
- Search deals by destination, platform, or travel type
- Filter deals by price range
- Sort deals by any field
- Track recently viewed deals
- View the most popular (most viewed) deals
- Track overall API usage statistics
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
│   ├── deal_routes.py        # All deal endpoints
│   └── stats_routes.py       # API usage statistics endpoint
├── services/
│   ├── deal_service.py       # Business logic for deals
│   └── stats_service.py      # Business logic for usage statistics
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
git clone https://github.com/tamim-cste/travel_deals_management_system_Farman_Arefin_Tamim.git
cd travel_deals_management_system_Farman_Arefin_Tamim
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

Deal IDs are auto-incrementing integers (e.g. `1`, `2`, `3`), assigned by the database when a deal is created.

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
**Success → 201**
```json
{
  "success": true,
  "message": "Travel deal created successfully.",
  "data": {
    "id": 7,
    "destination": "Dubai",
    "price": 5000.0,
    "platform": "Booking",
    "rating": 4.5,
    "travel_type": "Luxury",
    "view_count": 0,
    "created_at": "2026-06-16T11:45:35.590865Z",
    "updated_at": "2026-06-16T11:45:35.590869Z"
  }
}
```
**Validation Error → 422**

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
Each call increments that deal's `view_count` and adds it to the recently-viewed list.

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
- Every `destination` search is counted towards `most_searched_destination` in `/stats`

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

### 8. Update a Travel Deal
```
PUT /deals/<deal_id>
```
**Request Body:** same shape and validation rules as `POST /deals` — this is a full replacement, not a partial update, so all 5 fields are required even if you're only changing one of them.
```json
{
  "destination": "Canada",
  "price": 210000,
  "platform": "Airbnb",
  "rating": 5,
  "travel_type": "Luxury"
}
```
**Success → 200**
```json
{
  "success": true,
  "message": "Travel deal updated successfully.",
  "data": {
    "id": 2,
    "destination": "Canada",
    "price": 210000.0,
    "platform": "Airbnb",
    "rating": 5.0,
    "travel_type": "Luxury",
    "view_count": 5,
    "created_at": "2026-06-16T09:05:15.948683Z",
    "updated_at": "2026-06-16T11:45:35.686527Z"
  }
}
```
**Validation Error → 422** | **Not Found → 404**

---

### 9. Delete a Travel Deal
```
DELETE /deals/<deal_id>
```
**Success → 200** | **Not Found → 404**

---

### 10. Most Viewed Deals
```
GET /deals/popular
GET /deals/popular?limit=5
```
Returns deals ranked by `view_count` (descending). `limit` is optional and defaults to 10.

**Success → 200** | **Validation Error → 422**

---

### 11. API Usage Statistics
```
GET /stats
```
Returns:
```json
{
  "success": true,
  "message": "API usage statistics retrieved successfully.",
  "data": {
    "total_requests": 83,
    "successful_requests": 70,
    "failed_requests": 13,
    "most_searched_destination": { "destination": "Canada", "search_count": 5 },
    "most_viewed_deal": {
      "id": 2,
      "destination": "Canada",
      "view_count": 5,
      "...": "..."
    }
  }
}
```
`total_requests` counts every request the API has received (across all endpoints, including this one). `most_searched_destination` and `most_viewed_deal` are `null` until at least one search/view has happened.

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

### Deal Update
Identical rules to Deal Creation above — `PUT /deals/<deal_id>` requires the full payload, not a partial one. An invalid `deal_id` returns a `404`, separately from any `422` validation errors on the body.

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

### Popular Deals
| Param | Rule |
|---|---|
| `limit` | Optional, must be a positive integer if provided (default `10`) |

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

## How Statistics Are Tracked

- **View count** — `Deal.view_count` increments every time `GET /deals/<id>` is called for that deal. `GET /deals/popular` ranks deals by this value.
- **Search count** — every `GET /deals/search` call that includes a `destination` parameter increments a counter for that destination (case-insensitive) in the `search_stats` table. `/stats` reports whichever destination has the highest count.
- **Request count** — a Flask `after_request` hook (wired in `app.py`, logic in `services/stats_service.py`) runs after every request and increments `total_requests`, plus either `successful_requests` (status `< 400`) or `failed_requests` (status `>= 400`) in the single-row `api_stats` table.

---

## Logging

All API activity is logged to `logs/app.log` and printed to the terminal.

| Level | When used |
|---|---|
| `INFO` | Successful operations |
| `WARNING` | Validation errors, empty searches |
| `ERROR` | Missing request body, resource not found |
