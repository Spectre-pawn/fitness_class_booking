
# Fitness Studio Booking API

A Django REST API for managing fitness class bookings with timezone support.

## Features

- List upcoming fitness classes with timezone conversion
- Book classes with validation and race condition protection
- View bookings by email
- Comprehensive error handling and logging
- Unit tests included

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. Create sample data:
   ```bash
   python manage.py create_sample_data
   ```

4. Run the server:
   ```bash
   python manage.py runserver
   ```



## Timezone Support

- All classes are stored in IST `(Asia/Kolkata)`
- API supports timezone conversion via query parameters
- Automatic timezone handling for different client locations
"""

## Scenario 1: Complete Booking Flow

List available classes `(GET /api/classes/)`
Pick a class ID from the response
Create a booking `(POST /api/book/)` using that class ID
Verify booking `(GET /api/bookings/)` with your email
Check class again `(GET /api/classes/)` - available slots should decrease

## Scenario 2: Error Testing

Try booking same class twice - should get duplicate error
Try booking with invalid class_id - should get `"Class not found"`
Try booking without email - should get validation error
Try getting bookings without email parameter - should get error

## Scenario 3: Timezone Testing

Get classes in IST `(default)`
Get classes in EST `(?timezone=America/New_York)`
Get classes in GMT `(?timezone=Europe/London)`
Compare datetime vs datetime_local fields




## API Usage Guide in cammand promt :git bash

### Base URL
```
http://127.0.0.1:8000/api/
```

---

## 1.List Available Classes

### Endpoint: `GET /api/classes/`

**Basic Usage:**
```bash
curl -X GET "http://127.0.0.1:8000/api/classes/"
```

**With Timezone Conversion:**
```bash
# Convert to New York timezone
curl -X GET "http://127.0.0.1:8000/api/classes/?timezone=America/New_York"

# Convert to London timezone
curl -X GET "http://127.0.0.1:8000/api/classes/?timezone=Europe/London"
```


## 2.Create a Booking

### Endpoint: `POST /api/book/`

**Using cURL:**
```bash
curl -X POST "http://127.0.0.1:8000/api/book/" \
  -H "Content-Type: application/json" \
  -d '{
    "class_id": 1,
    "client_name": "kunal barve",
    "client_email": "kunal@gmail.com.com"
  }'
```
---

## 3.View Your Bookings

### Endpoint: `GET /api/bookings/?email=your@email.com`

**Using cURL:**
```bash
curl -X GET "http://127.0.0.1:8000/api/bookings/?email=kunal@gmail.com"
```



---
## Method 2: Using Postman

#### 1. GET Classes

**Request Setup:**
- **Method:** GET
- **URL:** `http://127.0.0.1:8000/api/classes/`
- **Headers:** 
  ```
  Content-Type: application/json
  ```

**Query Parameters (Optional):**
- Key: `timezone`
- Value: `America/New_York` (or any valid timezone)


#### 2. POST Create Booking

**Request Setup:**
- **Method:** POST
- **URL:** `http://127.0.0.1:8000/api/book/`
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (JSON):**
  ```json
  {
      "class_id": 1,
      "client_name": "kunal barve",
      "client_email": "kunal@gmail.com"
  }
  ```




#### 3.GET Bookings by Email

**Request Setup:**
- **Method:** GET
- **URL:** `http://127.0.0.1:8000/api/bookings/`
- **Query Parameters:**
  - Key: `email`
  - Value: `msdhoni@email.com`

**Full URL:** `http://127.0.0.1:8000/api/bookings/?email=msdhoni@email.com`
