# Tekton Python Concept

This document provides an in-depth explanation of a conceptual Product Inventory API powered by Python FastAPI, PostgreSQL, Redis, running over a set of Docker containers.

## Setup

In order to run this project, docker and docker-compose must be installed.

Once those dependencies are met, setup is done in two steps:

1. Run `docker-compose up db` in the root directory
2. Run `docker-compose up --build api`, also in the root directory

This will run four containers, as specified in `compose.yaml`:

- Products (Main) API: This is the main products API, whose functional requirements are specified in the Challenge document. It is developed using Python FastAPI and runs on port 8080 by default. Please refer to the specific API docs for detailed information on API endpoints. This documentation can be found under `http://localhost:8080/docs` once the application is deployed. The reader can also refer to `openapi.yaml` file using any swagger editor like the one in [`https://editor.swagger.io/`](https://editor.swagger.io/).
- Discounts (Mock) API: This API only has one endpoint which generates a random discount percentage value given a product id.
- Relational DB (PostgreSQL): This relational DB stores product data and allows Products API to perform queries on it.
- Cache (Redis): This cache is used to store a dictionary of status names, as specified in point 2.2 of the Challenge document.

# Containerized Services

The use of docker-compose and containers in this app allows for a really easy setup and teardown of all of the services involved. This is especially useful for a local Proof of Concept, but it could also easily be deployed to production if needed.

The four containerized services are explained in depth below:

## Products API

This API is the heart of the requested backend. It is a layered ReST API powered by Python FastAPI, featuring usage of Dependency Injection and the Repository Pattern. As mentioned above, documentation for this API can be found in the file `openapi.yaml` in the root directory.

### Folder Structure

The project is separated into 3 major layers, which are:

#### <b>Presentation Layer</b>

This layer includes both routers and layers. In fact, in FastAPI, controller logic is directly defined under route specifications, as can be seen in the files present under `$project_root/api/routers`. We'll be referring to the contents of that folder as routers or controllers interchangeably for the rest of this document.

This layer is the interface between the part of the application that contains business logic (see [Business Layer](#business-layer)).
Here, and more specifically in the controllers, the parameters sent by the user are processed and validated (the schemas for these are defined under `$project_root/api/interfaces`), and any reply from the server is serialized (using serializers present in `$project_root/api/serializers`) accordingly.

The controllers in this layer communicate do not contain any business logic and instead delegate it to the services, which they communicate with using dependency injection.

Serializers, in turn, transform the data received from the Business layer in a way it satisfies the needs of the clients. For example, the final price is calculated based on the price and discount provided by the business layer, but not present in the latter.

#### <b>Business Layer </b>

This part of the application is almost entirely contained in the `$project_root/api/services` folder, also using interfaces for domain models specified in the interfaces folder. In this case, the only domain model present in `Product` (`$project_root/api/interfaces/product.py`).

As can clearly be seen, all of the business logic regarding the contents of created and modified data is determined here. Domain models are used to seamlessly communicate with Presentation and Repository layers, avoiding the use of Data Access Objects (DAOs) outside the latter layer. This is showcased in `ProductsService` (`$project_root/api/services/products.py`).
But there can also be wrappers of services present in external servers. This is the case of `DiscountsService`, a wrapper that provides an interface and logic for interacting with the [Discounts Mock API](#discounts-mock-api).

#### <b>Repository Layer</b>

This layer, in itself, showcases the importance of the use of the repository API and how it could contribute to creating reusable code.

Tables are modelled through the use of data access objects (DAOs, also known as "Models" in the literature, although this term is not used in this document since it collides with "(Domain) Models" used in the Business Layer).

All insertion logic is present in a Repository class, one for each domain. In this case, there is only one domain (Products) and only one Repository (ProductsRepository). Ideally, methods in a repository are limited to the CRUD methods on data from and to one or multiple data sources, with no further modifications.

Separation of concerns with the business layer is shown by using only Domain Models in the interfaces of the Repositories, yet converting them to and from DAOs in order to perform reads and writes from and to the database.

### Dependency Injection

FastAPI has built-in dependency injection. This design allows to reuse components without having to re-instantiate them.

It also decouples the application modules throughout domains and different layers.

This also makes the code more readable, and makes unit testing easier, since dependencies can be mocked in most frameworks.

## Discounts (Mock) API

Instead of using 3rd party software with limited functionality, the simplicity of `docker-compose` and FastAPI is used to create this one-endpoint API that generates a random discount number (from 0 to 100) given a product ID. This can further be customized and extended, for example, to make the distribution of random numbers more natural instead of just using a uniform distribution. 

## Products DB (PostgreSQL)

This PostgreSQL DB contains only one table, created using alembic migrations. Alembic, by the way, is a Python library that allows to create migrations on dbs, which is really useful in this case. These migrations are executed upon the creation of the Products API Container.

The table has the following structure:
```
                                       Table "public.products"
   Column    |          Type           | Collation | Nullable |               Default                
-------------+-------------------------+-----------+----------+--------------------------------------
 id          | integer                 |           | not null | nextval('products_id_seq'::regclass)
 name        | character varying(256)  |           | not null | 
 status      | integer                 |           | not null | 
 stock       | integer                 |           | not null | 
 description | character varying(1024) |           |          | 
 price       | integer                 |           | not null | 

Indexes:
    "products_pkey" PRIMARY KEY, btree (id)
    "ix_products_id" btree (id)
    "products_name_key" UNIQUE CONSTRAINT, btree (name)
```

## Redis Cache


# Tests

Unit tests are defined at the router level and are implemented using pytest, a Python unit testing framework.

In the test configuration (`$project_root/tests/conftest.py`), DB dependencies are replaced by custom ones.

- In the case of the Products DB, a dedicated tests DB is used (that is, the db is not mocked, following unit testing best practices), and it is created before and destroyed after each test, as specified in the app fixture.
- In the case of the Cache, it is replaced by a mock class that has the same interface as the Redis SDK for Python (`hmget` and `hmset` functions).

