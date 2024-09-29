# Company Network API

This project is a Django-based API for managing a network of companies and their relationships,
using Neo4j as the database backend.

## Technologies Used

-   Django 3.2.10
-   Django REST Framework 3.12.4
-   Neo4j (via neomodel 4.0.8)
-   Docker
-   Gunicorn
-   drf-yasg (for API documentation)

## Prerequisites

-   Docker and Docker Compose
-   A Neo4j database instance (cloud-hosted or local)

## Setup and Installation

1. Clone the repository:

```
    git clone https://github.com/eniiku/company-network.git
    cd company-network
```

2. Create a `.env` file in the project root with the following content:

```
    NEO4J_CONNECTION_URI=your_instance_id.databases.neo4j.io
    NEO4J_USERNAME=neo4j
    NEO4J_PASSWORD=your_neo4j_password

    DJANGO_SECRET_KEY=your_secret_key_here
    DEBUG=False
```

3. Build and start the Docker containers:

```
    docker-compose up --build
```

The API should now be running at `http://localhost:8000`.

## API Documentation

Once the server is running, you can access the API documentation at:

-   Swagger UI: `http://localhost:8000/swagger/`
-   ReDoc: `http://localhost:8000/redoc/`

## Database Initialization

The database is automatically initialized with sample data when the Docker container starts. If
you need to manually initialize or reset the database, you can run:

```
    docker-compose run web
    python manage.py populate_db
```

## Deployment

This project is containerized and can be deployed to any platform that supports Docker. Make sure to set the appropriate environment variables for your production environment.
