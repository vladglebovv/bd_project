from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from flask import request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:LizaLiza199!!@localhost:5432/shop_api"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class ProductImages(db.Model):
	__tablename__ = 'product_images'
	id = db.Column(db.Integer, primary_key=True)
	product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
	title = db.Column(db.String(), nullable=False)
	filename = db.Column(db.String(), nullable=False)

class ProductPrices(db.Model):
	__tablename__ = 'product_prices'
	product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
	period = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	price = db.Column(db.Integer, nullable=False)

	__table_args__ = (
        db.PrimaryKeyConstraint(product_id, period),
        {},
    )

class PropertyValues(db.Model):
	__tablename__ = 'property_values'
	property_id = db.Column(db.Integer, db.ForeignKey('product_category_properties.id'), nullable=False)
	product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
	value = db.Column(db.String(), nullable=False)

	__table_args__ = (
        db.PrimaryKeyConstraint(property_id, product_id),
        {},
    )

class PropertyValueReferences(db.Model):
	__tablename__ = 'property_value_references'
	id = db.Column(db.Integer, nullable=False)
	property_id = db.Column(db.Integer, db.ForeignKey('product_category_properties.id'), nullable=False)
	value = db.Column(db.Integer, nullable=False)

	__table_args__ = (
        db.PrimaryKeyConstraint(id, property_id),
        {},
    )

class Products(db.Model):
	__tablename__ = 'products'
	id = db.Column(db.Integer, primary_key=True)
	category_id = db.Column(db.Integer, db.ForeignKey('product_categories.id'), nullable=False)
	title = db.Column(db.String(), nullable=False)
	description = db.Column(db.String(), nullable=False)

class ProductCategories(db.Model):
	__tablename__ = 'product_categories'
	id = db.Column(db.Integer, primary_key=True)
	parent_id = db.Column(db.Integer, db.ForeignKey('product_categories.id'))
	title = db.Column(db.String(), nullable=False)

class ProductCategoryProperties(db.Model):
	__tablename__ = 'product_category_properties'
	id = db.Column(db.Integer, primary_key=True)
	parent_id = db.Column(db.Integer, db.ForeignKey('product_category_properties.id'))
	category_id = db.Column(db.Integer, db.ForeignKey('product_categories.id'), nullable=False)
	title = db.Column(db.String(), nullable=False)
	property_type = db.Column(db.String(), nullable=False)


@app.route('/product-categories', methods=['POST', 'GET'])
def handle_product_categories():
	if request.method == 'POST':
		if request.is_json:
			data = request.get_json()
			if 'parent_id' in data:
				new_product_category = ProductCategories(parent_id=data['parent_id'], title=data['title'])
			else:
				new_product_category = ProductCategories(title=data['title'])
			db.session.add(new_product_category)
			db.session.commit()
			return {"message": f"new_product_category {new_product_category.title} has been created successfully."}
		else:
			return {"error": "The request payload is not in JSON format"}

	elif request.method == 'GET':
		product_categories = ProductCategories.query.all()
		results = [
					{
					"id": category.id,
					"parent_id": category.parent_id,
					"title": category.title
					} 
				for category in product_categories]
		return {"count": len(results), "product_categories": results}



@app.route('/product-category-properties', methods=['POST', 'GET'])
def handle_product_category_properties():
	if request.method == 'POST':
		if request.is_json:
			data = request.get_json()
			if 'parent_id' in data:
				new_product_category_property = ProductCategoryProperties(parent_id=data['parent_id'], category_id=data['category_id'], title=data['title'], property_type=data['property_type'])
			else:
				new_product_category_property = ProductCategoryProperties(category_id=data['category_id'], title=data['title'], property_type=data['property_type'])
			db.session.add(new_product_category_property)
			db.session.commit()
			return {"message": f"new_product_category_property {new_product_category_property.title} has been created successfully."}
		else:
			return {"error": "The request payload is not in JSON format"}

	elif request.method == 'GET':
		product_category_properties = ProductCategoryProperties.query.all()
		results = [
					{
					"id": category_property.id,
					"parent_id": category_property.parent_id,
					"category_id": category_property.category_id,
					"title": category_property.title,
					"property_type": category_property.property_type
					} 
				for category_property in product_category_properties]
		return {"count": len(results), "product_category_properties": results}




@app.route('/products', methods=['POST', 'GET'])
def handle_products():
	if request.method == 'POST':
		if request.is_json:
			data = request.get_json()
			new_product = Products(category_id=data['category_id'], title=data['title'], description=data['description'])
			db.session.add(new_product)
			db.session.commit()
			return {"message": f"new_product {new_product.title} has been created successfully."}
		else:
			return {"error": "The request payload is not in JSON format"}

	elif request.method == 'GET':
		products = Products.query.all()
		results = [
					{
					"id": product.id,
					"category_id": product.category_id,
					"title": product.title,
					"description": product.description
					} 
				for product in products]
		return {"count": len(results), "products": results}




@app.route('/product-images', methods=['POST', 'GET'])
def handle_product_images():
	if request.method == 'POST':
		if request.is_json:
			data = request.get_json()
			new_product_image = ProductImages(product_id=data['product_id'], title=data['title'], filename=data['filename'])
			db.session.add(new_product_image)
			db.session.commit()
			return {"message": f"new_product_image {new_product_image.filename} has been created successfully."}
		else:
			return {"error": "The request payload is not in JSON format"}
	elif request.method == 'GET':
		product_images = ProductImages.query.all()
		results = [
					{
					"id": product_image.id,
					"product_id": product_image.product_id,
					"title": product_image.title,
					"filename": product_image.filename
					} 
				for product_image in product_images]
		return {"count": len(results), "product_images": results}


@app.route('/product-prices', methods=['POST', 'GET'])
def handle_product_prices():
	if request.method == 'POST':
		if request.is_json:
			data = request.get_json()
			if 'period' in data:
				new_product_price = ProductPrices(product_id=data['product_id'], price=data['price'], period=data['period'])
			else:
				new_product_price = ProductPrices(product_id=data['product_id'], price=data['price'])
			db.session.add(new_product_price)
			db.session.commit()
			return {"message": f"new_product_price product_id {new_product_price.product_id} {new_product_price.price}$ has been created successfully."}
		else:
			return {"error": "The request payload is not in JSON format"}

	elif request.method == 'GET':
		product_prices = ProductPrices.query.all()
		results = [
					{
					"product_id": product_price.product_id,
					"price": product_price.price,
					"period": product_price.period
					} 
				for product_price in product_prices]
		return {"count": len(results), "product_prices": results}







@app.route('/property-values', methods=['POST', 'GET'])
def handle_property_values():
	if request.method == 'POST':
		if request.is_json:
			data = request.get_json()
			new_property_value = PropertyValues(property_id=data['property_id'], product_id=data['product_id'], value=data['value'])
			db.session.add(new_property_value)
			db.session.commit()
			return {"message": f"new_property_value property_id {new_property_value.property_id} product_id {new_property_value.product_id} value {new_property_value.value} has been created successfully."}
		else:
			return {"error": "The request payload is not in JSON format"}

	elif request.method == 'GET':
		property_values = PropertyValues.query.all()
		results = [
					{
					"property_id": property_value.property_id,
					"product_id": property_value.product_id,
					"value": property_value.value
					} 
				for property_value in property_values]
		return {"count": len(results), "property_values": results}





@app.route('/products-route', methods=['GET'])
def handle_products_route():
	if request.method == 'GET':
		query = db.session.query(Products, ProductCategories, ProductImages, ProductPrices)
		query = query.join(ProductCategories, Products.category_id == ProductCategories.id)
		query = query.join(ProductImages, Products.id == ProductImages.product_id)
		query = query.join(ProductPrices, Products.id == ProductPrices.product_id)
		if request.is_json:
			data = request.get_json()
			if 'product_category' in data: query = query.filter(ProductCategories.title == data['product_category'])
			if 'product_title' in data: query = query.filter(Products.title == data['product_title'])
			if 'product_price_min' in data: query = query.filter(ProductPrices.price >= data['product_price_min'])
			if 'product_price_max' in data: query = query.filter(ProductPrices.price <= data['product_price_max'])
		records = query.all()
		results = [
					{
						"product_id": product.id,
						"product_title": product.title,
						"product_description": product.description,
						"product_category": category.title,
						"product_image": image.filename,
						"product_price": price.price,
						"product_price_date": price.period
					}
				for product, category, image, price in records]
		return {"count": len(results), "products_route": results}
			

@app.route('/product-id-route', methods=['POST', 'GET'])
def handle_product_id_route():
	if request.method == 'GET':
		if request.is_json:
			data = request.get_json()
			query = db.session.query(Products, ProductCategoryProperties, PropertyValues, ProductCategories, ProductImages, ProductPrices) 
			query = query.outerjoin(PropertyValues, Products.id == PropertyValues.product_id)
			query = query.outerjoin(ProductCategoryProperties, PropertyValues.property_id == ProductCategoryProperties.id)
			query = query.join(ProductCategories, Products.category_id == ProductCategories.id)
			query = query.join(ProductImages, Products.id == ProductImages.product_id)
			query = query.join(ProductPrices, Products.id == ProductPrices.product_id)
			
			query = query.filter(Products.id == data['product_id'])
			records = query.all()
			results = [
					{
						"property_title": property_.title,
						"property_value": property_value.value, 
					}
				for product, property_, property_value, category, image, price in records if property_value is not None]
			images = ProductImages.query.filter_by(product_id=data['product_id']).all()
			price = ProductPrices.query.filter_by(product_id=data['product_id']).order_by(ProductPrices.period).first()
			image_list = [{"img_title": image.title, "img_path": image.filename} for image in images]
			return {
						"id": records[0].Products.id,
						"title": records[0].Products.title,
						"description": records[0].Products.description, 
						"category": records[0].ProductCategories.title, 
						"price": price.price, 
						"image": image_list, 
						"properties": results
					}
	if request.method == 'POST':
		if request.is_json:
			data = request.get_json()
			if "category" in data and "description" in data and "title" in data and "price" in data and str(data["price"]).isdigit():
				state = (ProductCategories.query.filter_by(title=data['category']).first() == None)
				if state:
					return {"result": "Invalid category"}
				else:
					new_product = Products(category_id=ProductCategories.query.filter_by(title=data['category']).first().id, title=data['title'], description=data['description'])
					db.session.add(new_product)
					db.session.commit()

					new_product_price = ProductPrices(product_id=new_product.id, price=data['price'])
					db.session.add(new_product_price)
					db.session.commit()

					if "image" in data:
						for i in data["image"]:
							if "img_path" in i and "img_title" in i:
								new_product_image = ProductImages(product_id=new_product.id, title=i['img_title'], filename=i['img_path'])
								db.session.add(new_product_image)
								db.session.commit()

					if "properties" in data:
						proper = ProductCategoryProperties.query.filter_by(category_id=ProductCategories.query.filter_by(title=data['category']).first().id)
						for i in data["properties"]:
							if "property_title" in i and "property_value" in i:
								state = (proper.filter_by(title=i["property_title"]).first() == None)
								if state == False:
									new_property = PropertyValues(property_id=proper.filter_by(title=i["property_title"]).first().id, product_id=new_product.id, value=i["property_value"])
									db.session.add(new_property)
									db.session.commit()

					return {"result": f"new product #{new_product.id} has been created successfully"}
				#ProductCategories.query.filter_by(title=data['category']).first()
if __name__ == '__main__':
    app.run(debug=True)
