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
- ## 🚀 API Endpoints

### Category
- **POST** `/categories/add` → Add a category  
- **GET** `/categories` → Get all categories  
- **PUT** `/categories/<id>` → Update category by ID  
- **DELETE** `/categories/<id>` → Delete category by ID  

### Product
- **POST** `/products/add` → Add a product  
- **GET** `/products` → Get all products  
- **PUT** `/products/<id>` → Update product by ID  
- **DELETE** `/products/<id>` → Delete product by ID  

### Attributes
- **POST** `/attributes/add` → Add attribute to product  
- **GET** `/products/<id>` → Get product details with attributes  


## Run
```bash
pip install -r requirements.txt
python app.py
# open http://127.0.0.1:5000/health
```
