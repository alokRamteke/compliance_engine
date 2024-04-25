## This is a very small, ultra-simplified, non-AI version of compliance engine


## Installation

1. Clone the repository:
   ```
   git clone https://github.com/alokRamteke/compliance_engine.git
   ```

2. Navigate to the project directory:
    ```
    cd compliance_engine/
    ```

3. Create a virtual environment:
   ```
   virtualenv -p python3.12 venv
   ```
4. Activate the virtual environment:
   ```
   source venv/bin/activate
   ```

5. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

6. Create a .env file in the project root directory:
    ```
    touch .env
    ````

7. Add the following environment variables to the .env file:
    ```
    SECRET_KEY=your_secret_key_here
    DB_NAME=your_database_name
    DB_USER=your_database_user
    DB_PASSWORD=your_database_password
    DB_HOST=your_database_host
    DB_PORT=your_database_port
    ```

8. Apply database migrations:
    ```
    python manage.py migrate
    ```

9. Start the development server:
    ```
    python manage.py runserver
    ```

## API endpoints are organized in the following groups:

### Guideline endpoints

- `GET /guidelines/` - Retrieves all Guideline instances.
- `POST /guidelines/` - Creates a new Guideline instance.
- `PATCH /guidelines/<guideline_id>/` - Updates a Guideline instance.
- `PUT /guidelines/<guideline_id>/` - Updates a Guideline instance.

### Content endpoints

- `GET /contents/` - Retrieves all Content instances.
- `POST /contents/upload/` - Uploads new Content instance.
- `GET /contents/<content_id>/` - Retrieves a specific Content instance.
- `PATCH /contents/<content_id>/` - Updates a specific Content instance.
- `PUT /contents/<content_id>` - Updates a specific Content instance.
- `GET /contents/<content_id>/review-status/` - Retrieves status of review items for a specific content.
- `PUT /contents/<content_id>/review/<review_item_id>/` - Updates a ReviewItem instance for a specific content.

Requests parameters:

- All endpoints expect JSON data.
- All endpoints expect the `Authorization` header to be set with a valid Bearer token.

Request responses:

- Successful requests return a JSON object with the updated data.
- Error requests return a JSON object with an `error` key indicating the error message.

## API Documentation

The API documentation is generated using both Swagger and ReDoc.

- Swagger UI: You can access the Swagger UI by navigating to /swagger/ in your browser.
- ReDoc: Alternatively, you can access the ReDoc documentation by navigating to /redoc/ in your browser.
