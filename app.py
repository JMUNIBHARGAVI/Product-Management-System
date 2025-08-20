from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pmt.db'  # Database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==============================
# Database Models
# ==============================

# ==============================
# Database Models  (REPLACE THIS WHOLE SECTION)
# ==============================

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    # relationships
    attributes = db.relationship("Attribute", backref="category", cascade="all, delete-orphan")
    products   = db.relationship("Product",   backref="category", cascade="all, delete-orphan")


class Attribute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)

    # NEW line — keep it separate (don’t append it to the previous line)
    attribute_values = db.relationship(
        "ProductAttributeValue",
        backref="product",
        cascade="all, delete-orphan"
    )


class ProductAttributeValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    attribute_id = db.Column(db.Integer, db.ForeignKey("attribute.id"), nullable=False)
    value = db.Column(db.String(200), nullable=False)

    # relationships (so you can use val.attribute.name)
    attribute = db.relationship("Attribute", backref="attribute_values")


# ==============================
# Routes
# ==============================

@app.route("/")
def home():
    return "Welcome to Product Management Tool API! Try /categories, /products"


# --- Categories ---
@app.route("/categories", methods=["GET"])
def get_categories():
    categories = Category.query.all()
    return jsonify([{"id": c.id, "name": c.name} for c in categories])

@app.route("/categories/add", methods=["POST"])
def add_category():
    data = request.json
    new_cat = Category(name=data["name"])
    db.session.add(new_cat)
    db.session.commit()
    return jsonify({"message": "Category added", "id": new_cat.id})


# --- Attributes ---
@app.route("/categories/<int:cat_id>/attributes", methods=["GET"])
def get_attributes(cat_id):
    attrs = Attribute.query.filter_by(category_id=cat_id).all()
    return jsonify([{"id": a.id, "name": a.name} for a in attrs])

@app.route("/categories/<int:cat_id>/attributes/add", methods=["POST"])
def add_attribute(cat_id):
    data = request.json
    new_attr = Attribute(name=data["name"], category_id=cat_id)
    db.session.add(new_attr)
    db.session.commit()
    return jsonify({"message": "Attribute added", "id": new_attr.id})


# --- Products ---
@app.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    result = []
    for p in products:
        values = {
            val.attribute.name: val.value for val in p.attribute_values
        }
        result.append({
            "id": p.id,
            "name": p.name,
            "category": p.category.name,
            "attributes": values
        })
    return jsonify(result)

@app.route("/products/add", methods=["POST"])
def add_product():
    data = request.json
    category = Category.query.get(data["category_id"])
    if not category:
        return jsonify({"error": "Invalid category"}), 400

    new_product = Product(name=data["name"], category_id=data["category_id"])
    db.session.add(new_product)
    db.session.commit()


    # Add attributes
    for attr_id, value in data.get("attributes", {}).items():
        pav = ProductAttributeValue(
            product_id=new_product.id,
            attribute_id=int(attr_id),
            value=value
        )
        db.session.add(pav)
    db.session.commit()

    return jsonify({"message": "Product added", "id": new_product.id})

# Update product
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.json or {}

    if "name" in data:
        product.name = data["name"]
    if "category_id" in data:
        product.category_id = data["category_id"]

    if "attributes" in data:
        # remove old attribute values for this product
        ProductAttributeValue.query.filter_by(product_id=product.id).delete()

        # add new ones
        for attr_id, value in data["attributes"].items():
            db.session.add(ProductAttributeValue(
                product_id=product.id,
                attribute_id=int(attr_id),
                value=value
            ))

    db.session.commit()

    return jsonify({"message": "Product updated successfully"})


# Delete product
@app.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"})



# ==============================
# Run Setup
# ==============================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Creates tables if not exist
    app.run(debug=True)
