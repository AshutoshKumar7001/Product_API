from flask import Blueprint, request, jsonify
from .models import Product, db
from .schemas import ProductSchema

product_bp = Blueprint("product_bp", __name__)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

@product_bp.route('/products', methods=['Get'])
def get_products():
    products= Product.query.all()
    return products_schema(many= True)

@product_bp.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return product_schema.jsonify(product)

@product_bp.route('/products', methods=['POST'])
def create_product():
    data = request.json
    new_product = product_schema.load(data)
    db.session.commit()
    return product_schema.jsonify(new_product), 201

@product_bp.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product= Product.query.get_or_404(id)
    data = request.json
    for key, value in data.items():
        setattr(product, key, value)
    db.session.commit()
    return product_schema.jsonify(product)

@product_bp.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted'})