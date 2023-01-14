import json
import math

from api.data_access_objects.product import ProductDAO

def test_create_product(client):
    data = {
        "name": "TV",
        "status": 0,
        "stock": 54,
        "description": "Simple appliance",
        "price": 100000
    }
    response = client.post("/products/",content=json.dumps(data))
    assert response.status_code == 201
    assert response.json()["name"] == "TV"
    assert response.json()["id"] != None

def test_create_repeated_product(client, db_session):
    existing_product = ProductDAO(
        name="TV-2",
        status=0,
        stock=54,
        description="No need to go to the cinema",
        price=100000
    )
    db_session.add(existing_product)
    db_session.commit()
    data = {
        "name": "TV-2",
        "status": 1,
        "stock": 50,
        "description": "Just a TV",
        "price": 1000
    }
    response = client.post("/products/",content=json.dumps(data))
    assert response.status_code == 422

def test_create_products_with_missing_fields(client):
    incomplete_product_1 = {
        "name": "TV",
        "description": "Simple appliance",
        "price": 100000
    }
    incomplete_product_2 = {
        "status": 0,
        "stock": 54,
        "price": 100000
    }
    response_1 = client.post("/products/",content=json.dumps(incomplete_product_1))
    response_2 = client.post("/products/",content=json.dumps(incomplete_product_2))
    assert response_1.status_code == 422
    assert response_2.status_code == 422

def test_update_product(client, db_session):
    product_1 = ProductDAO(
        name= "TV",
        status= 1,
        stock= 54,
        description= "Simple appliance",
        price= 100000
    )
    db_session.add(product_1)
    db_session.commit()
    db_session.refresh(product_1)
    editable_data = {
        "status": 'Active',
        "stock": 0,
        "description": "Simple appliance - or maybe not so simple",
        "price": 200000
    }
    response = client.patch(f"/products/{product_1.id}", content=json.dumps(editable_data))
    assert response.status_code == 202
    edited_product = db_session.query(ProductDAO).filter(ProductDAO.id == product_1.id).first()
    assert edited_product.status == 1
    assert edited_product.stock == editable_data["stock"]
    assert edited_product.description == editable_data["description"]
    assert edited_product.price == editable_data["price"]

def test_update_non_existent_product(client):
    editable_data = {
        "status": 'Active',
        "stock": 0,
        "description": "Simple appliance - or maybe not so simple",
        "price": 200000
    }
    response = client.patch(f"/products/1", content=json.dumps(editable_data))
    assert response.status_code == 404

def test_update_product_with_conflicting_name(client, db_session):
    product_1 = ProductDAO(
        name= "TV",
        status= 0,
        stock= 54,
        description= "Simple appliance",
        price= 100000
    )
    db_session.add(product_1)
    db_session.commit()
    db_session.refresh(product_1)
    product_2 = ProductDAO(
        name= "Big TV",
        status= 0,
        stock= 54,
        description= "Big simple appliance",
        price= 150000
    )
    db_session.add(product_2)
    db_session.commit()
    db_session.refresh(product_2)
    editable_data = {
        "name": "TV",
        "status": 'Active',
        "stock": 0,
        "description": "Simple appliance - or maybe not so simple",
        "price": 200000
    }
    response = client.patch(f"/products/{product_2.id}", content=json.dumps(editable_data))
    assert response.status_code == 422

def test_update_products_with_bad_fields(client, db_session):
    product_1 = ProductDAO(
        name= "TV",
        status= 0,
        stock= 54,
        description= "Simple appliance",
        price= 100000
    )
    db_session.add(product_1)
    db_session.commit()
    db_session.refresh(product_1)
    product_2 = ProductDAO(
        name= "Big TV",
        status= 0,
        stock= 54,
        description= "Big simple appliance",
        price= 150000
    )
    db_session.add(product_2)
    db_session.commit()
    db_session.refresh(product_2)

    product_with_non_modifiable_fields = {
        "id": product_2.id
    }
    response_1 = client.patch(f"/products/{product_1.id}",content=json.dumps(product_with_non_modifiable_fields))
    assert response_1.json()["id"] == product_1.id

def test_get_product(client, db_session):
    product_1 = ProductDAO(
        name= "TV",
        status= 0,
        stock= 54,
        description= "Simple appliance",
        price= 100000
    )
    db_session.add(product_1)
    db_session.commit()
    db_session.refresh(product_1)

    response = client.get(f'/products/{product_1.id}')

    assert response.json()["id"] == product_1.id
    assert response.json()["name"] == product_1.name
    assert response.json()["status"] == 'Inactive' if product_1.status == 0 else 'Active'
    assert response.json()["stock"] == product_1.stock
    assert response.json()["description"] == product_1.description
    assert response.json()["price"] == product_1.price
    

def test_get_non_existent_product(client):
    response = client.get(f'/products/1')
    assert response.status_code == 404
