import json

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
        name="TV",
        status=0,
        stock=54,
        description="No need to go to the cinema",
        price=100000
    )
    db_session.add(existing_product)
    data = {
        "name": "TV",
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

def test_update_product(client):
    data = {
        "name": "TV",
        "status": 0,
        "stock": 54,
        "description": "Simple appliance",
        "price": 100000
    }
    product_1_response = client.post("/products/",content=json.dumps(data))
    editable_data = {
        "status": 1,
        "stock": 0,
        "description": "Simple appliance - or maybe not so simple",
        "price": 200000
    }
    response = client.patch(f"/products/{product_1_response.json()['id']}", content=json.dumps(editable_data))
    assert response.status_code == 401
    edited_product = client.get(f"/products/{product_1_response.json()['id']}").json()
    assert edited_product["status"] == editable_data["status"]
    assert edited_product["stock"] == editable_data["stock"]
    assert edited_product["description"] == editable_data["description"]
    assert edited_product["price"] == editable_data["price"]

def test_update_non_existent_product(client):
    editable_data = {
        "status": 1,
        "stock": 0,
        "description": "Simple appliance - or maybe not so simple",
        "price": 200000
    }
    response = client.patch(f"/products/1", content=json.dumps(editable_data))
    assert response.status_code == 404

def test_update_product_with_conflicting_name(client):
    data_1 = {
        "name": "TV",
        "status": 0,
        "stock": 54,
        "description": "Simple appliance",
        "price": 100000
    }
    product_1_response = client.post("/products/",content=json.dumps(data_1))
    data_2 = {
        "name": "Big TV",
        "status": 0,
        "stock": 54,
        "description": "Big simple appliance",
        "price": 150000
    }
    product_2_response = client.post("/products/",content=json.dumps(data_2))
    editable_data = {
        "name": "TV",
        "status": 1,
        "stock": 0,
        "description": "Simple appliance - or maybe not so simple",
        "price": 200000
    }
    response = client.patch(f"/products/{product_2_response.json()['id']}", content=json.dumps(editable_data))
    assert response.status_code == 422

def test_update_products_with_bad_fields(clients):
    assert True

def test_get_product(clients):
    assert True

def test_get_non_existent_product(client):
    assert True