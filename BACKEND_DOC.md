# week4_fleet — Backend API Documentation

> Written for student developers.  
> This project is a **REST API backend** built with Flask and PostgreSQL. There is no frontend yet. Bruno is used to manually test all endpoints.

---

## Table of Contents

1. [What This Project Does](#1-what-this-project-does)
2. [Tech Stack](#2-tech-stack)
3. [How the Architecture Works](#3-how-the-architecture-works)
4. [Database Schema (ERD)](#4-database-schema-erd)
5. [Project File Structure](#5-project-file-structure)
6. [How to Run the Project](#6-how-to-run-the-project)
7. [Base URL](#7-base-url)
8. [API Endpoints](#8-api-endpoints)
   - [Health Check](#health-check)
   - [Driver Endpoints](#driver-endpoints)
   - [Vehicle Endpoints](#vehicle-endpoints)
   - [Route Endpoints](#route-endpoints)
   - [Package Endpoints](#package-endpoints)
9. [How Bruno Testing Works](#9-how-bruno-testing-works)
10. [Error Responses](#10-error-responses)
11. [Key Concepts for Beginners](#11-key-concepts-for-beginners)

---

## 1. What This Project Does

`week4_fleet` is a **fleet management backend API**. It manages:

- **Drivers** — people who drive vehicles and are assigned to routes
- **Vehicles** — trucks or cars assigned to one driver
- **Routes** — delivery routes assigned to a driver on a specific date
- **Packages** — parcels that belong to a route

You can **Create, Read, Update, and Delete** (CRUD) records for all four of these resources using HTTP requests.

---

## 2. Tech Stack

| Tool | What It Does |
|---|---|
| **Python** | The programming language |
| **Flask** | The web framework — creates the API and handles HTTP requests |
| **PostgreSQL** | The database — stores all the data |
| **psycopg2** | The Python library that connects Flask to PostgreSQL |
| **python-dotenv** | Loads secret database credentials from the `.env` file |
| **Bruno** | API testing tool — acts as the temporary frontend to send requests |

---

## 3. How the Architecture Works

Since there is no frontend yet, Bruno fills that role during development.

```
Bruno (API Tester)
      ↓
  HTTP Request (GET, POST, PUT, DELETE)
      ↓
Flask Routes (routes/driver.py, vehicle.py, route.py, package.py)
      ↓
psycopg2 (executes SQL queries)
      ↓
PostgreSQL Database (fleet schema)
      ↓
Flask returns JSON response
      ↓
Bruno displays the result
```

**In plain English:**
- You send a request in Bruno (e.g., `GET /driver`)
- Flask receives it and runs a SQL query via psycopg2
- PostgreSQL returns the data
- Flask sends it back as JSON
- Bruno shows you the JSON

---

## 4. Database Schema (ERD)

### Relationships

| Relationship | Type | Explanation |
|---|---|---|
| Driver → Vehicle | **1:1** | One driver owns one vehicle. Enforced by `UNIQUE` on `driver_id` in the vehicle table. |
| Driver → Route | **1:N** | One driver can be assigned to many routes (different days). |
| Route → Package | **1:N** | One route can carry many packages. |

### Tables

**DRIVER**
| Column | Type | Notes |
|---|---|---|
| `driver_id` | SERIAL | Primary Key, auto-increments |
| `name` | VARCHAR(100) | Driver's full name |
| `license_type` | VARCHAR(50) | e.g. "Class A", "Class B" |

**VEHICLE**
| Column | Type | Notes |
|---|---|---|
| `vehicle_id` | SERIAL | Primary Key, auto-increments |
| `license_plate` | VARCHAR(20) | Plate number |
| `model` | VARCHAR(100) | e.g. "Ford Transit" |
| `driver_id` | INT | Foreign Key → `fleet.driver`. `UNIQUE` enforces the 1:1 relationship |

**ROUTE**
| Column | Type | Notes |
|---|---|---|
| `route_id` | SERIAL | Primary Key, auto-increments |
| `date` | DATE | The date the route runs |
| `service_zone` | VARCHAR(100) | e.g. "North Zone" |
| `driver_id` | INT | Foreign Key → `fleet.driver`. No UNIQUE — one driver can have many routes |

**PACKAGE**
| Column | Type | Notes |
|---|---|---|
| `package_id` | SERIAL | Primary Key, auto-increments |
| `description` | TEXT | What the package contains |
| `weight` | DECIMAL | Weight in your chosen unit |
| `route_id` | INT | Foreign Key → `fleet.route` |

> **Why is `driver_id` in Route and not just in Package?**  
> Because a route is assigned to a specific driver on a specific day. The driver is responsible for the whole route, not individual packages.

---

## 5. Project File Structure

```
week4_fleet/
│
├── app.py              # Entry point — creates the Flask app and registers blueprints
├── database.py         # Database connection and table creation (init_db)
├── requirements.txt    # Python dependencies
├── .env                # Secret credentials (DB host, user, password) — never commit this
│
├── routes/
│   ├── __init__.py     # Makes routes/ a Python package
│   ├── driver.py       # All /driver endpoints
│   ├── vehicle.py      # All /vehicle endpoints
│   ├── route.py        # All /route endpoints
│   └── package.py      # All /package endpoints
│
├── driver/             # Bruno collection files for driver
├── vehicle/            # Bruno collection files for vehicle
└── venv/               # Python virtual environment (do not edit)
```

### What is a Blueprint?
Flask **Blueprints** let you split your routes into separate files. In `app.py`, each blueprint is registered with a URL prefix:

```python
app.register_blueprint(driver, url_prefix="/driver")
app.register_blueprint(vehicle, url_prefix="/vehicle")
app.register_blueprint(route, url_prefix="/route")
app.register_blueprint(package, url_prefix="/package")
```

This means all functions inside `routes/driver.py` automatically start with `/driver`.

---

## 6. How to Run the Project

```bash
# 1. Activate your virtual environment
venv\Scripts\activate          # Windows CMD
source venv/bin/activate       # Mac/Linux

# 2. Install dependencies (first time only)
pip install -r requirements.txt

# 3. Make sure your .env file has the correct database credentials

# 4. Run the Flask server
python app.py
```

You should see:
```
Database Ready!
 * Running on http://127.0.0.1:5000
```

---

## 7. Base URL

```
http://127.0.0.1:5000
```

All endpoints below are relative to this base URL.

---

## 8. API Endpoints

---

### Health Check

#### `GET /`

Confirms the server is running.

**Request:** No body needed.

**Response `200 OK`:**
```json
{
  "message": "Server Online"
}
```

---

### Driver Endpoints

Base path: `/driver`

---

#### `GET /driver/` — Get All Drivers

Retrieves every driver in the database.

**Request:** No body needed.

**Response `200 OK`:**
```json
[
  {
    "driver_id": 1,
    "name": "Sarah",
    "license_type": "Class B"
  },
  {
    "driver_id": 2,
    "name": "Marcus",
    "license_type": "Class A"
  }
]
```

**SQL executed:**
```sql
SELECT * FROM fleet.driver;
```

---

#### `POST /driver/` — Create a Driver

Adds a new driver to the database.

**Request Body (JSON):**
```json
{
  "name": "Sarah",
  "license_type": "Class B"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | Yes | Driver's full name |
| `license_type` | string | Yes | License class (e.g. "Class A", "Class B") |

**Response `201 Created`:**
```json
{
  "message": "Object Created"
}
```

**SQL executed:**
```sql
INSERT INTO fleet.driver (name, license_type)
VALUES ('Sarah', 'Class B');
```

---

#### `PUT /driver/<id>` — Update a Driver

Updates an existing driver by their `driver_id`.

**URL Parameter:**
- `<id>` — the `driver_id` of the driver you want to update (integer)

**Example URL:** `PUT /driver/1`

**Request Body (JSON):**
```json
{
  "name": "Sarah Johnson",
  "license_type": "Class A"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | Yes | Updated name |
| `license_type` | string | Yes | Updated license class |

**Response `201`:**
```json
{
  "message": "Object Updated"
}
```

**SQL executed:**
```sql
UPDATE fleet.driver
SET name = 'Sarah Johnson', license_type = 'Class A'
WHERE driver_id = 1;
```

---

#### `DELETE /driver/<id>` — Delete a Driver

Deletes a driver by their `driver_id`.

**URL Parameter:**
- `<id>` — the `driver_id` of the driver to delete (integer)

**Example URL:** `DELETE /driver/1`

**Request Body:** None

**Response `201`:**
```json
{
  "message": "Object Deleted"
}
```

**SQL executed:**
```sql
DELETE FROM fleet.driver
WHERE driver_id = 1;
```

> **Important:** If a vehicle or route references this driver via a foreign key, the delete will fail with a database error. You must delete or reassign those records first.

---

### Vehicle Endpoints

Base path: `/vehicle`

---

#### `GET /vehicle/` — Get All Vehicles

Retrieves every vehicle in the database.

**Request:** No body needed.

**Response `200 OK`:**
```json
[
  {
    "vehicle_id": 1,
    "license_plate": "ABC-1234",
    "model": "Ford Transit",
    "driver_id": 1
  }
]
```

**SQL executed:**
```sql
SELECT * FROM fleet.vehicle;
```

---

#### `POST /vehicle/` — Create a Vehicle

Adds a new vehicle and assigns it to a driver.

**Request Body (JSON):**
```json
{
  "license_plate": "ABC-1234",
  "model": "Ford Transit",
  "driver_id": 1
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `license_plate` | string | Yes | The vehicle's plate number |
| `model` | string | Yes | Vehicle make/model |
| `driver_id` | integer | Yes | Must match an existing `driver_id`. Must be unique — one driver, one vehicle. |

**Response `201 Created`:**
```json
{
  "message": "Object Created"
}
```

**SQL executed:**
```sql
INSERT INTO fleet.vehicle (license_plate, model, driver_id)
VALUES ('ABC-1234', 'Ford Transit', 1);
```

> **Note:** If you try to assign a `driver_id` that already has a vehicle, PostgreSQL will reject it because of the `UNIQUE` constraint. This enforces the 1:1 relationship.

---

#### `PUT /vehicle/<id>` — Update a Vehicle

Updates an existing vehicle by its `vehicle_id`.

**Example URL:** `PUT /vehicle/1`

**Request Body (JSON):**
```json
{
  "license_plate": "XYZ-9999",
  "model": "Mercedes Sprinter",
  "driver_id": 2
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `license_plate` | string | Yes | Updated plate number |
| `model` | string | Yes | Updated model |
| `driver_id` | integer | Yes | Updated driver assignment |

**Response `201`:**
```json
{
  "message": "Object Updated"
}
```

**SQL executed:**
```sql
UPDATE fleet.vehicle
SET license_plate = 'XYZ-9999', model = 'Mercedes Sprinter', driver_id = 2
WHERE vehicle_id = 1;
```

---

#### `DELETE /vehicle/<id>` — Delete a Vehicle

Deletes a vehicle by its `vehicle_id`.

**Example URL:** `DELETE /vehicle/1`

**Request Body:** None

**Response `201`:**
```json
{
  "message": "Object Deleted"
}
```

**SQL executed:**
```sql
DELETE FROM fleet.vehicle
WHERE vehicle_id = 1;
```

---

### Route Endpoints

Base path: `/route`

---

#### `GET /route/` — Get All Routes

Retrieves every route in the database.

**Request:** No body needed.

**Response `200 OK`:**
```json
[
  {
    "route_id": 1,
    "date": "Mon, 12 May 2025 00:00:00 GMT",
    "service_zone": "North Zone",
    "driver_id": 1
  }
]
```

> **Note:** PostgreSQL DATE fields are returned as a full datetime string by Flask/psycopg2.

**SQL executed:**
```sql
SELECT * FROM fleet.route;
```

---

#### `POST /route/` — Create a Route

Assigns a driver to a route on a specific date and zone.

**Request Body (JSON):**
```json
{
  "date": "2025-05-12",
  "service_zone": "North Zone",
  "driver_id": 1
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `date` | string | Yes | Date in `YYYY-MM-DD` format |
| `service_zone` | string | Yes | Name of the delivery zone |
| `driver_id` | integer | Yes | Must match an existing `driver_id` |

**Response `201 Created`:**
```json
{
  "message": "Object Created"
}
```

**SQL executed:**
```sql
INSERT INTO fleet.route (date, service_zone, driver_id)
VALUES ('2025-05-12', 'North Zone', 1);
```

> **Note:** The same driver can appear in multiple routes on different dates. There is no `UNIQUE` constraint on `driver_id` here — this is what makes it a 1:N relationship.

---

#### `PUT /route/<id>` — Update a Route

Updates an existing route by its `route_id`.

**Example URL:** `PUT /route/1`

**Request Body (JSON):**
```json
{
  "date": "2025-05-15",
  "service_zone": "South Zone",
  "driver_id": 2
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `date` | string | Yes | Updated date (`YYYY-MM-DD`) |
| `service_zone` | string | Yes | Updated zone |
| `driver_id` | integer | Yes | Updated driver |

**Response `201`:**
```json
{
  "message": "Object Updated"
}
```

**SQL executed:**
```sql
UPDATE fleet.route
SET date = '2025-05-15', service_zone = 'South Zone', driver_id = 2
WHERE route_id = 1;
```

---

#### `DELETE /route/<id>` — Delete a Route

Deletes a route by its `route_id`.

**Example URL:** `DELETE /route/1`

**Request Body:** None

**Response `201`:**
```json
{
  "message": "Object Deleted"
}
```

**SQL executed:**
```sql
DELETE FROM fleet.route
WHERE route_id = 1;
```

> **Important:** If packages reference this route via `route_id`, the delete will fail. Delete the packages first.

---

### Package Endpoints

Base path: `/package`

---

#### `GET /package/` — Get All Packages

Retrieves every package in the database.

**Request:** No body needed.

**Response `200 OK`:**
```json
[
  {
    "package_id": 1,
    "description": "Electronics - fragile",
    "weight": 2.5,
    "route_id": 1
  }
]
```

**SQL executed:**
```sql
SELECT * FROM fleet.package;
```

---

#### `POST /package/` — Create a Package

Adds a new package and assigns it to a route.

**Request Body (JSON):**
```json
{
  "description": "Electronics - fragile",
  "weight": 2.5,
  "route_id": 1
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `description` | string | Yes | What the package contains |
| `weight` | number (decimal) | Yes | Weight of the package |
| `route_id` | integer | Yes | Must match an existing `route_id` |

**Response `201 Created`:**
```json
{
  "message": "Object Created"
}
```

**SQL executed:**
```sql
INSERT INTO fleet.package (description, weight, route_id)
VALUES ('Electronics - fragile', 2.5, 1);
```

---

#### `PUT /package/<id>` — Update a Package

Updates an existing package by its `package_id`.

**Example URL:** `PUT /package/1`

**Request Body (JSON):**
```json
{
  "description": "Clothing - standard",
  "weight": 1.2,
  "route_id": 2
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `description` | string | Yes | Updated description |
| `weight` | number (decimal) | Yes | Updated weight |
| `route_id` | integer | Yes | Updated route assignment |

**Response `201`:**
```json
{
  "message": "Object Updated"
}
```

**SQL executed:**
```sql
UPDATE fleet.package
SET description = 'Clothing - standard', weight = 1.2, route_id = 2
WHERE package_id = 1;
```

---

#### `DELETE /package/<id>` — Delete a Package

Deletes a package by its `package_id`.

**Example URL:** `DELETE /package/1`

**Request Body:** None

**Response `201`:**
```json
{
  "message": "Object Deleted"
}
```

**SQL executed:**
```sql
DELETE FROM fleet.package
WHERE package_id = 1;
```

---

## 9. How Bruno Testing Works

Bruno is an API client (similar to Postman) that lets you send HTTP requests to your Flask server without a frontend.

### Steps to test an endpoint in Bruno

1. Make sure your Flask server is running (`python app.py`)
2. Open Bruno and select your collection
3. Choose the request you want to test (e.g., `POST /driver/`)
4. If it's a POST or PUT, go to the **Body** tab and enter your JSON
5. Click **Send**
6. The response appears in the panel on the right

### Example: Creating a driver in Bruno

- Method: `POST`
- URL: `http://127.0.0.1:5000/driver/`
- Body (JSON):
```json
{
  "name": "Sarah",
  "license_type": "Class B"
}
```
- Expected response:
```json
{
  "message": "Object Created"
}
```

### Recommended testing order

Because of foreign key relationships, you must create records in this order:

```
1. Create a Driver first
2. Create a Vehicle (needs driver_id)
3. Create a Route (needs driver_id)
4. Create a Package (needs route_id)
```

If you try to create a Vehicle before a Driver exists, PostgreSQL will reject it with a foreign key error.

---

## 10. Error Responses

All endpoints use a `try/except` block. If something goes wrong, Flask returns:

**Response `500 Internal Server Error`:**
```json
{
  "message": "An unexpected error occurred: <error details here>"
}
```

### Common causes of errors

| Error | Likely Cause |
|---|---|
| `foreign key violation` | You referenced a `driver_id` or `route_id` that doesn't exist |
| `unique constraint violation` | You tried to assign a `driver_id` to a second vehicle (1:1 rule broken) |
| `not null violation` | You forgot a required field in your JSON body |
| `connection refused` | Flask can't reach PostgreSQL — check your `.env` credentials |

---

## 11. Key Concepts for Beginners

### What is a REST API?
A REST API is a way for programs to communicate over HTTP. Your Flask app exposes **endpoints** (URLs) that accept requests and return JSON data.

### What is JSON?
JSON (JavaScript Object Notation) is the format used to send and receive data. It looks like a Python dictionary:
```json
{
  "name": "Sarah",
  "license_type": "Class B"
}
```

### What is a Primary Key (PK)?
A unique ID for each row in a table. In this project, all PKs are `SERIAL`, meaning PostgreSQL automatically assigns the next number (1, 2, 3...).

### What is a Foreign Key (FK)?
A column that references the PK of another table. For example, `driver_id` in the `vehicle` table points to `driver_id` in the `driver` table. This links the two records together.

### What does UNIQUE do?
The `UNIQUE` constraint on `driver_id` in the `vehicle` table means no two vehicles can share the same driver. This is how the **1:1 relationship** is enforced at the database level.

### What is psycopg2?
It's the Python library that lets your Flask code talk to PostgreSQL. It sends SQL queries and returns the results as Python data.

### What is `RealDictCursor`?
By default, psycopg2 returns rows as plain tuples like `(1, "Sarah", "Class B")`. `RealDictCursor` makes it return rows as dictionaries like `{"driver_id": 1, "name": "Sarah", "license_type": "Class B"}`, which Flask can then convert to proper JSON.

### What is a Blueprint?
A Flask Blueprint is a way to organize routes into separate files. Instead of putting all 16 endpoints in one giant `app.py`, each resource (driver, vehicle, route, package) has its own file. They are all connected back to the main app in `app.py` using `register_blueprint`.

---

*Documentation written for week4_fleet — Flask + PostgreSQL Backend API*
