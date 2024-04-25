## This is a very small, ultra-simplified, non-AI version of compliance engine

API endpoints are organized in the following groups:

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
