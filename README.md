# Coderr Backend

<p align="center">
  <img src="assets/logo_coderr.svg" width="150"/>
</p>

## 🚀 About the Project

Coderr is the backend of a freelancer developer platform. The frontend was already developed, and the goal of this project is to implement the backend logic and connect both parts into a fully working application.

The backend provides a REST API for all core platform features such as authentication, user profiles, offers, orders, reviews, and general platform data.

---

## ✨ Features

* User registration and login
* Authentication system
* User profile management
* Offer creation and management
* Order system
* Review system
* Base information endpoint
* REST API for frontend integration

---

## 🛠️ Tech Stack

* Python
* Django
* Django REST Framework
* SQLite / PostgreSQL
* Git & GitHub

---

## 🌐 API Endpoints

### 🔐 Authentication

* `POST /api/registration/` — Register a new user
* `POST /api/login/` — Log in a user

---

### 📦 Offers

* `GET /api/offers/` — Get all offers

* `POST /api/offers/` — Create a new offer

* `GET /api/offers/<id>/` — Get a specific offer

* `PUT /api/offers/<id>/` — Update an offer

* `PATCH /api/offers/<id>/` — Partially update an offer

* `DELETE /api/offers/<id>/` — Delete an offer

* `GET /api/offerdetails/<id>/` — Get pricing tier details

---

### 🛒 Orders

* `GET /api/orders/` — Get all orders

* `POST /api/orders/` — Create a new order

* `GET /api/orders/<id>/` — Get a specific order

* `PUT /api/orders/<id>/` — Update an order

* `DELETE /api/orders/<id>/` — Delete an order

* `GET /api/order-count/<business_user_id>/` — Get active orders count

* `GET /api/completed-order-count/<business_user_id>/` — Get completed orders count

---

### 👤 Profile

* `GET /api/profile/<user_id>/` — Get user profile

* `PUT /api/profile/<user_id>/` — Update profile

* `PATCH /api/profile/<user_id>/` — Partially update profile

* `GET /api/profiles/business/` — Get all business profiles

* `GET /api/profiles/customer/` — Get all customer profiles

---

### ⭐ Reviews

* `GET /api/reviews/` — Get all reviews
* `POST /api/reviews/` — Create a review
* `GET /api/reviews/<id>/` — Get a specific review
* `PUT /api/reviews/<id>/` — Update a review
* `DELETE /api/reviews/<id>/` — Delete a review

---

### ℹ️ Base Info

* `GET /api/base-info/` — Get platform base information

---

## ⚙️ Installation

```bash
git clone https://github.com/your-username/coderr-backend.git
cd coderr-backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Server runs on:
http://127.0.0.1:5500/

---

## 🔐 Environment Variables

Create a `.env` file in the root directory:

```
SECRET_KEY=your-secret-key
DEBUG=True
```

Make sure `.env` is in `.gitignore`.

---

## 📁 Project Structure

```
project/
 ├── core/
 |  ├──settings.py
 |  ├──urls.py
 |  ├──views.py
 |  ├──wsgi.py
 |  └──asgi.py
 ├── auth_app/
 ├── offers_app/
 ├── orders_app/
 ├── reviews_app/
 ├── profile_app/
 ├── manage.py
 ├── README.md
 └── requirements.txt
```

---

## 🚧 Status

This project is part of a full-stack application and is actively in development.

---

## 👨‍💻 Author

Your Name
GitHub: https://github.com/Takoua852/

---

## 📄 License

This project is for educational purposes.
