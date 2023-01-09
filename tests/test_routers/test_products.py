import json


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

def test_create_repeated_product(client):
    existing_product = {
        "name": "TV",
        "status": 0,
        "stock": 54,
        "description": "No need to go to the cinema",
        "price": 100000
    }
    data = {
        "name": "TV",
        "status": 1,
        "stock": 50,
        "description": "Just a TV",
        "price": 1000
    }
    client.post('/products/',content=json.dumps(existing_product))
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
    # product_1_response = client.post("/products/",content=json.dumps(data))
    # editable_data = {
    #     "status": 1,
    #     "stock": 0,
    #     "description": "Simple appliance - or maybe not so simple",
    #     "price": 200000
    # }
    # response = client.patch(f"/products/{product_1_response.json()['id']}", content=json(editable_data))
    # assert response.status_code == 401
    # edited_product = client.get(f"/products/{product_1_response.json()['id']}").json()
    # assert edited_product["status"] == editable_data["status"]
    # assert edited_product["stock"] == editable_data["stock"]
    # assert edited_product["description"] == editable_data["description"]
    # assert edited_product["price"] == editable_data["price"]
