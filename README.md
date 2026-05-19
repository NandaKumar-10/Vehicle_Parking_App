# 🚗 Vehicle Parking App

A full-stack web application for managing vehicle parking lots and spot reservations, built with **Flask** and **SQLite** .

---

## 📋 Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [Application Routes](#application-routes)
- [Setup & Installation](#setup--installation)
- [Running the App](#running-the-app)
- [Usage](#usage)
- [Default Admin Credentials](#default-admin-credentials)

---

## About the Project

The **Vehicle Parking App** is a multi-role web application that allows an **Admin** to manage parking lots and spots, while **Users** can register, book parking spots, and view their booking history and costs. The system automatically calculates parking costs based on the duration of stay.

---

## ✨ Features

### 👤 User Features
- User Registration & Secure Login
- Browse available parking spots by city and location
- Book a parking spot with vehicle number
- Release a booked spot and view the calculated cost
- View recent booking history on the dashboard
- Edit profile and change password
- View personal booking summary with cost breakdown

### 🛠️ Admin Features
- Admin account auto-created on first launch
- View and manage all parking lots (Add / Edit / Delete)
- Add and manage parking spots within lots
- View all registered users and their booking details
- Search users by ID, name, or email
- Search parking lots by ID, city, or location name
- View overall summary — total spots, occupied vs. available, and revenue per user

---

## 🛠️ Tech Stack

| Layer        | Technology                          |
|--------------|-------------------------------------|
| Backend      | Python 3, Flask 3.0.0               |
| Database     | SQLite (via Flask-SQLAlchemy 3.1.1) |
| ORM          | SQLAlchemy (Declarative Mapping)    |
| Forms        | Flask-WTF                           |
| Auth         | bcrypt 4.1.2 (password hashing)     |
| Frontend     | HTML5, Jinja2 Templates, CSS, JS    |
| Validation   | email-validator                     |

---

## 📁 Project Structure

```
parking_app_23f3001984/
│
├── app.py                          # Application entry point
├── requirements.txt                # Python dependencies
│
├── controllers/
│   ├── routes.py                   # All URL routes and view logic
│   ├── forms.py                    # WTForms form definitions
│   └── appFunctions.py             # Helper functions (e.g., price calculation)
│
├── models/
│   ├── __init__.py
│   └── model.py                    # SQLAlchemy database models
│
├── templates/                      # Jinja2 HTML templates
│   ├── base.html                   # Base layout template
│   ├── login.html                  # Login page
│   ├── register.html               # User registration page
│   ├── Userdashboard.html          # User dashboard
│   ├── AdminDashboard.html         # Admin dashboard
│   ├── AddParkingLot.html          # Add new parking lot (Admin)
│   ├── EditParkingLot.html         # Edit parking lot (Admin)
│   ├── AddingParkingSpot.html      # Add parking spot (Admin)
│   ├── EditParkingSpot.html        # Edit/delete parking spot (Admin)
│   ├── ViewUsers.html              # View all users (Admin)
│   ├── AdminSearch.html            # Search users/lots (Admin)
│   ├── AdminSummary.html           # Admin analytics summary
│   ├── UserBookingLot.html         # Spot booking page (User)
│   ├── UserSummary.html            # User booking summary
│   ├── release_spot.html           # Release spot confirmation
│   └── editprofile.html            # Edit user profile
│
└── static/
    ├── Style.css                   # Global stylesheet
    ├── AdminSummary.js             # Chart/summary scripts (Admin)
    ├── UserSummary.js              # Chart/summary scripts (User)
    └── images/                     # Static image assets
```

---

## 🗄️ Database Schema

The application uses **SQLite** with the following models:

### `Admin`
| Column   | Type    | Constraints              |
|----------|---------|--------------------------|
| id       | Integer | Primary Key              |
| email    | String  | Unique, Not Null         |
| name     | String  | Not Null                 |
| password | String  | Hashed with bcrypt       |

### `User`
| Column   | Type    | Constraints              |
|----------|---------|--------------------------|
| id       | Integer | Primary Key              |
| email    | String  | Unique, Not Null         |
| name     | String  | Not Null                 |
| password | String  | Hashed with bcrypt       |
| address  | String  | Not Null                 |
| pincode  | String  | Not Null                 |

### `Parking_Lot`
| Column              | Type    | Constraints    |
|---------------------|---------|----------------|
| id                  | Integer | Primary Key    |
| city                | String  | Not Null       |
| prime_location_name | String  | Not Null       |
| price               | Integer | Not Null       |
| address             | String  | Not Null       |
| pincode             | String  | Not Null       |
| max_no_spots        | Integer | Not Null       |
| no_spot_occupied    | Integer | Default: 0     |

### `Parking_Spot`
| Column  | Type    | Constraints                         |
|---------|---------|-------------------------------------|
| id      | Integer | Primary Key                         |
| lot_id  | Integer | FK → Parking_Lot (CASCADE DELETE)   |
| status  | String  | `'A'` = Available, `'O'` = Occupied |

### `Reserve_Parking_Spot`
| Column             | Type     | Constraints                        |
|--------------------|----------|------------------------------------|
| id                 | Integer  | Primary Key                        |
| spot_id            | Integer  | FK → Parking_Spot (CASCADE DELETE) |
| user_id            | Integer  | FK → User                          |
| Parking_timestamp  | DateTime | Not Null                           |
| Leaving_timestamp  | DateTime | Nullable                           |
| parking_cost       | Integer  | Nullable                           |
| vehicle_no         | String   | Not Null                           |
| occupancy          | String   | Default: `'Occupied'`              |

### `Booking_records`
| Column            | Type     | Constraints        |
|-------------------|----------|--------------------|
| id                | Integer  | Primary Key        |
| user_id           | Integer  | FK → User          |
| lot_id            | Integer  | FK → Parking_Lot   |
| spot_id           | Integer  | FK → Parking_Spot  |
| location_name     | String   | FK → Parking_Lot   |
| price             | Integer  | Nullable           |
| parking_timestamp | DateTime | Not Null           |
| leaving_timestamp | DateTime | Nullable           |
| vehicle_no        | String   | Not Null           |

---

## 🌐 Application Routes

| Method   | Route                                        | Description                         | Access  |
|----------|----------------------------------------------|-------------------------------------|---------|
| GET/POST | `/`                                          | Auto-create admin & redirect        | Public  |
| GET/POST | `/login` or `/home`                          | Login page                          | Public  |
| GET/POST | `/register`                                  | User registration                   | Public  |
| GET/POST | `/dashboard`                                 | User/Admin dashboard                | Auth    |
| GET/POST | `/dashboard/release_spot/<booking_id>`       | Release a booked spot               | User    |
| GET/POST | `/dashboard/bookspot/<user_id>`              | Book a parking spot                 | User    |
| GET/POST | `/dashboard/edit-profile`                    | Edit user profile/password          | User    |
| GET      | `/dashboard/summary`                         | Analytics summary                   | Both    |
| GET/POST | `/dashboard/AddParkingLot`                   | Add a new parking lot               | Admin   |
| GET/POST | `/dashboard/AddParkingSpot`                  | Add a spot to an existing lot       | Admin   |
| GET/POST | `/dashboard/editparkingLot/<lot_id>`         | Edit a parking lot                  | Admin   |
| GET/POST | `/dashboard/editparkingspot/<lot_id>`        | Edit/delete spots in a lot          | Admin   |
| GET      | `/dashboard/users`                           | View all users & their bookings     | Admin   |
| GET/POST | `/dashboard/search`                          | Search users or parking locations   | Admin   |
| GET      | `/logout`                                    | Logout and clear session            | Auth    |

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.8 or higher
- pip

### Steps

1. **Clone or extract the project:**
   ```bash
   cd parking_app_23f3001984
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   # source venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Running the App

```bash
python app.py
```

The application will start in **debug mode** and be accessible at:

```
http://127.0.0.1:5000
```

The SQLite database (`database.db`) will be automatically created inside the `instance/` folder on first run, and the default admin account will be initialized.

---

## 📖 Usage

### As a User
1. Navigate to `http://127.0.0.1:5000`
2. Register a new account via the **Register** page
3. Log in with your credentials
4. From the **Dashboard**, click **Book a Spot** to reserve a parking spot by selecting your city, location, and entering your vehicle number
5. Active bookings appear on your dashboard — click **Release** to check out and view your cost
6. Visit the **Summary** page to see your full booking history

### As Admin
1. Log in with the default admin credentials (see below)
2. From the **Admin Dashboard**, manage parking lots — add, edit, or delete them
3. Navigate to individual lots to manage spots
4. Use the **Search** feature to find users or parking locations
5. Visit the **Summary** page to see occupancy stats and revenue per user

---

## 🔑 Default Admin Credentials

| Field    | Value                |
|----------|----------------------|
| Email    | `admin@parking.com`  |
| Password | `password`           |

> ⚠️ **Note:** Change the admin password and the `SECRET_KEY` in `app.py` before deploying to any production environment.
