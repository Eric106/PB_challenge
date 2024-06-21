# WEB API ([routes.py](./routes.py))

This document describes the routes available in the Flask application, including the methods, purpose, and expected responses. All responses and request bodies must be in JSON format. Routes requiring authentication are noted accordingly.

## Middleware

### `auth_required`
A decorator to ensure that a valid token is present in the request headers. If the token is missing or invalid, it returns a 401 Unauthorized response.

## Routes

### `"/" (root)`
- **Methods**: POST, GET
- **Description**: Returns a simple success message.
- **Response** (JSON):
  - Success: `{ "success": True, "message": "hola mundo" }`, Status Code: 200

### `"/create_user"`
- **Methods**: POST
- **Description**: Creates a new user with the provided `user_name` and `password`.
- **Request Body** (JSON):
  - `user_name`: string
  - `password`: string
- **Response** (JSON):
  - Success: `{ "success": True }`, Status Code: 200
  - Error: `{ "message": "Bad Request" }`, Status Code: 400
  - Unauthorized: `{ "message": "Unauthorized" }`, Status Code: 401

### `"/delete_user"` (Requires Authentication)
- **Methods**: DELETE
- **Description**: Deletes the authenticated user
- **Response** (JSON):
  - Success: `{ "success": True }`, Status Code: 200
  - Error: `{ "message": "Bad Request" }`, Status Code: 400
  - Unauthorized: `{ "message": "Unauthorized" }`, Status Code: 401

### `"/login"`
- **Methods**: POST
- **Description**: Authenticates a user and returns a token if successful.
- **Request Body** (JSON):
  - `user_name`: string
  - `password`: string
- **Response** (JSON):
  - Success: `{ "success": True, "token": <token> }`, Status Code: 200
  - Error: `{ "message": "Bad Request" }`, Status Code: 400
  - Unauthorized: `{ "message": "Unauthorized" }`, Status Code: 401

> NOTE 👁🕳👁: **Standard JSON response and request for < investment details >**
```json
{
  "date_last_update": "2024-06-20 21:11:31.992824",
  "investment_id": "5d156836-ea88-4827-9f16-77f4b361b412",
  "iva_pb_commission": "160.00",
  "iva_pb_commission_rate": "0.1600",
  "iva_var_pay_commission": "79.63",
  "iva_var_pay_commission_rate": "0.1600",
  "pay_method": "VISA/MC",
  "pb_commission": "1000.00",
  "pb_commission_rate": "0.0500",
  "pb_points": "1000.00",
  "total_investment": "20000.00",
  "total_to_pay": "20737.33",
  "user_id": "d4e56ada-469f-4ddf-9097-ee028123b567",
  "var_pay_commission": "497.70",
  "var_pay_commission_rate": "0.0240"
}
```

### `"/create_investment"` (Requires Authentication)
- **Methods**: POST
- **Description**: Creates a new investment.
- **Request Body** (JSON): JSON object containing investment details.
- **Response** (JSON):
  - Success: `{ "success": True, "investment": <investment_details> }`, Status Code: 200
  - Error: `{ "message": "Bad Request" }`, Status Code: 400
    - When you don't have enough pb_point, to apply or a bad request

### `"/calc_investment"` (Requires Authentication)
- **Methods**: POST
- **Description**: Calculates investment details based on provided data.
- **Request Body** (JSON):
  - `total_investment`: Decimal
  - `pb_points`: Decimal
  - `pay_method`: string
- **Response** (JSON):
  - Success: `{ "success": True, "investment": <investment_details> }`, Status Code: 200
  - Error: `{ "message": "Bad Request" }`, Status Code: 400

### `"/get_investment"` (Requires Authentication)
- **Methods**: GET
- **Description**: Retrieves details of a specific investment by ID.
- **Request Body** (JSON):
  - `investment_id`: string
- **Response** (JSON):
  - Success: `{ "success": True, "investment": <investment_details> }`, Status Code: 200
  - Error: `{ "message": "Bad Request" }`, Status Code: 400
  - Not Found: `{ "message": "Not Found" }`, Status Code: 404

### `"/get_investments"` (Requires Authentication)
- **Methods**: GET
- **Description**: Retrieves a list of all investments for the authenticated user.
- **Response** (JSON):
  - Success: `{ "success": True, "investments": <list_of_investments> }`, Status Code: 200
  - Error: `{ "message": "Bad Request" }`, Status Code: 400

### `"/update_investment"` (Requires Authentication)
- **Methods**: POST
- **Description**: Updates an existing investment.
- **Request Body** (JSON): JSON object containing updated investment details.
- **Response** (JSON):
  - Success: `{ "success": True, "investment": <updated_investment_details> }`, Status Code: 200
  - Error: `{ "message": "Bad Request" }`, Status Code: 400
  - Not Found: `{ "message": "Not Found" }`, Status Code: 404

### `"/delete_investment"` (Requires Authentication)
- **Methods**: DELETE
- **Description**: Deletes an investment by ID.
- **Request Body** (JSON):
  - `investment_id`: string
- **Response** (JSON):
  - Success: `{ "success": True, "investment": <deleted_investment_details> }`, Status Code: 200
  - Error: `{ "message": "Bad Request" }`, Status Code: 400
  - Not Found: `{ "message": "Not Found" }`, Status Code: 404
