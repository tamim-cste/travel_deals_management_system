# Travel Deal Management System

A simple REST API built with Flask and SQLite to manage travel deals.

---

## What This Project Does

This API lets you:
- Add a new travel deal
- View all available deals
- View details of a specific deal

---

## Tech Stack

- **Python 3**
- **Flask** — web framework
- **Flask-SQLAlchemy** — ORM for database
- **SQLite** — lightweight database

---

## Project Structure

```
project/
├── app.py                  # App entry point
├── routes/
│   └── deal_routes.py      # API endpoints
├── services/
│   └── deal_service.py     # Business logic
├── utils/
│   └── validators.py       # Input validation
├── database/
│   └── store.py            # Database models & queries
├── requirements.txt
└── README.md
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/tamim-cste/travel_deals_management_system.git
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
pip install -r requirements.txt
```

### 4. Run the server

```bash
python3 app.py
```

API will be running at: `http://127.0.0.1:5000`

---

## API Endpoints

### Add a Travel Deal
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
**Success Response (201):**
```json
{
  "success": true,
  "message": "Travel deal created successfully.",
  "data": {
    "id": "uuid",
    "destination": "Dubai",
    "price": 5000.0,
    "platform": "Booking",
    "rating": 4.5,
    "travel_type": "Luxury",
    "created_at": "2024-01-01T10:00:00Z"
  }
}
```

---

### Get All Deals
```
GET /deals
```
**Success Response (200):**
```json
{
  "success": true,
  "message": "Deals retrieved successfully.",
  "data": {
    "total": 2,
    "deals": [...]
  }
}
```

---

### Get Single Deal
```
GET /deals/<deal_id>
```
**Success Response (200):**
```json
{
  "success": true,
  "message": "Deal retrieved successfully.",
  "data": { ... }
}
```
**Not Found (404):**
```json
{
  "success": false,
  "message": "Deal with id 'abc' not found."
}
```

---

## Validation Rules

| Field | Rule |
|---|---|
| `destination` | Cannot be empty |
| `price` | Must be a positive number |
| `platform` | Cannot be empty |
| `rating` | Must be between 1 and 5 |
| `travel_type` | Must be one of: `Budget`, `Luxury`, `Adventure`, `Family` |

**Validation Error Response (422):**
```json
{
  "success": false,
  "message": "Validation failed.",
  "data": {
    "errors": ["'price' must be a positive number."]
  }
}
```

---

## HTTP Status Codes Used

| Code | Meaning |
|---|---|
| `200` | OK — request successful |
| `201` | Created — new deal added |
| `404` | Not Found — deal doesn't exist |
| `405` | Method Not Allowed |
| `422` | Unprocessable Entity — validation failed |
| `500` | Internal Server Error |

---

## Notes

- Data is saved in a local SQLite database (`instance/travel_deals.db`)
- Data persists even after restarting the server
- Import `postman_collection.json` in Postman to test all endpoints quickly
