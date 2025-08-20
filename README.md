# Product Management System (Flask + SQLAlchemy)

## 📌 Project Overview
This is a simple **Flask-based REST API** for managing categories, products, and product attributes.  
It demonstrates CRUD (Create, Read, Update, Delete) operations with a relational database using **Flask + SQLAlchemy**.

## 🚀 Features
- Add, view, update, and delete **Categories**
- Add, view, update, and delete **Products**
- Add attributes to products (e.g., size, color, etc.)
- Relational mapping between Categories → Products → Attributes
- REST API endpoints tested with **Postman**

## ⚙️ Tech Stack
- Python 3.x
- Flask
- Flask-SQLAlchemy
- SQLite (for demo, can be switched to MySQL/Postgres)
- Postman (for testing)

## Run
```bash
pip install -r requirements.txt
python app.py
# open http://127.0.0.1:5000/health
```
