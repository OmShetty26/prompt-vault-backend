***

### 2. Backend README (`prompt-vault-backend/README.md`)

# PromptVault API

A FastAPI backend handling data persistence, schema validation, and REST routing for the PromptVault application. 

*The React frontend repository for this project is located [here](https://github.com/OmShetty26/prompt-vault).*

## Tech Stack
* **Framework:** FastAPI (Python)
* **Server Engine:** Uvicorn
* **Database & ORM:** PostgreSQL / SQLAlchemy

## Architecture & Features
* **RESTful Endpoints:** Provides structured GET and POST routes to handle CRUD operations for prompt data payloads.
* **Relational Database Mapping:** Uses SQLAlchemy ORM models to define strict database schemas and handle data persistence.
* **CORS Configuration:** Explicitly configured middleware to accept cross-origin network requests from the decoupled local frontend environment.
* **Automatic Documentation:** Leverages FastAPI's built-in Swagger UI integration to automatically generate and host API documentation.

## Local Setup

1. Clone the [backend repository](https://github.com/OmShetty26/prompt-vault-backend.git):

```bash
git clone https://github.com/OmShetty26/prompt-vault-backend.git
cd prompt-vault-backend
```

2. Create and activate a Python virtual environment:
    Windows:
        ```bash
        python -m venv venv
        source venv/Scripts/activate
        ```

    Mac/Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3. Install the required dependencies:
    ```bash
    pip install fastapi uvicorn sqlalchemy
    ```

4. Start the Uvicorn server:
    ```bash
    uvicorn main:app --reload
    ```

5. The API will boot on [http://127.0.0.1:8000](http://127.0.0.1:8000). Navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to view the interactive API documentation. 
