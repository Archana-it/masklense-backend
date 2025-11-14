# MaskLens Backend API

Django REST API for facial analysis application with JWT authentication.

## Features

- User registration and authentication with JWT tokens
- Facial image upload and analysis
- Weekly summary generation
- User profile management
- Secure API endpoints

## Tech Stack

- Django 5.2.7
- Django REST Framework
- Simple JWT for authentication
- SQLite database (development)
- Pillow for image handling

## Installation

### Prerequisites

- Python 3.8+
- pip

### Setup

1. Install dependencies:
```bash
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers pillow
```

2. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Create superuser (optional):
```bash
python manage.py createsuperuser
```

4. Run development server:
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

---

## API Documentation

### Base URL
```
http://localhost:8000/api/
```

---

## Authentication Endpoints

### 1. Register User

**Endpoint:** `POST /api/auth/register/`

**Description:** Create a new user account

**Request Body:**
```json
{
  "email": "user@example.com",
  "full_name": "John Doe",
  "password": "securepassword123"
}
```

**Response:** `201 Created`
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "date_joined": "2025-11-10T10:30:00Z"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

**Error Response:** `400 Bad Request`
```json
{
  "email": ["User with this email already exists."],
  "password": ["This password is too short."]
}
```
hgjshfjkfkjdkjf

---

### 2. Login

**Endpoint:** `POST /api/auth/login/`

**Description:** Authenticate user and receive JWT tokens

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:** `200 OK`
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "date_joined": "2025-11-10T10:30:00Z"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

**Error Response:** `400 Bad Request`
```json
{
  "non_field_errors": ["Invalid credentials"]
}
```

---

### 3. Refresh Token

**Endpoint:** `POST /api/auth/token/refresh/`

**Description:** Get a new access token using refresh token

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:** `200 OK`
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## User Profile Endpoints

### 4. Get/Update User Profile

**Endpoint:** `GET/PUT/PATCH /api/user/profile/`

**Description:** Retrieve or update authenticated user's profile

**Headers:**
```
Authorization: Bearer <access_token>
```

**GET Response:** `200 OK`
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "date_joined": "2025-11-10T10:30:00Z"
}
```

**PUT/PATCH Request Body:**
```json
{
  "full_name": "John Smith"
}
```

**PUT/PATCH Response:** `200 OK`
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Smith",
  "date_joined": "2025-11-10T10:30:00Z"
}
```

---

## Facial Analysis Endpoints

### 5. Upload Image for Analysis

**Endpoint:** `POST /api/analysis/`

**Description:** Upload a masked facial image for analysis

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
```

**Request Body (Form Data):**
```
image: <file>
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "user": 1,
  "user_email": "user@example.com",
  "image": "/media/facial_images/image_2025_11_10.jpg",
  "analysis_result": {
    "skin_health": {
      "acne": "low",
      "dark_circles": "medium",
      "wrinkles": "low",
      "hydration": "good"
    },
    "recommendations": [
      "Use moisturizer daily",
      "Get adequate sleep",
      "Stay hydrated"
    ],
    "overall_score": 7.5
  },
  "created_at": "2025-11-10T10:30:00Z"
}
```

**Error Response:** `400 Bad Request`
```json
{
  "image": ["No file was submitted."]
}
```

---

### 6. Get All Analyses

**Endpoint:** `GET /api/analysis/list/`

**Description:** Retrieve all facial analyses for authenticated user

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
[
  {
    "id": 2,
    "user": 1,
    "user_email": "user@example.com",
    "image": "/media/facial_images/image_2025_11_10_2.jpg",
    "analysis_result": {
      "skin_health": {
        "acne": "low",
        "dark_circles": "medium",
        "wrinkles": "low",
        "hydration": "good"
      },
      "recommendations": [
        "Use moisturizer daily",
        "Get adequate sleep"
      ],
      "overall_score": 7.5
    },
    "created_at": "2025-11-10T14:30:00Z"
  },
  {
    "id": 1,
    "user": 1,
    "user_email": "user@example.com",
    "image": "/media/facial_images/image_2025_11_10.jpg",
    "analysis_result": {
      "skin_health": {
        "acne": "medium",
        "dark_circles": "high",
        "wrinkles": "low",
        "hydration": "fair"
      },
      "recommendations": [
        "Use eye cream",
        "Get more sleep"
      ],
      "overall_score": 6.8
    },
    "created_at": "2025-11-10T10:30:00Z"
  }
]
```

---

### 7. Get Single Analysis

**Endpoint:** `GET /api/analysis/<id>/`

**Description:** Retrieve a specific facial analysis by ID

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "user": 1,
  "user_email": "user@example.com",
  "image": "/media/facial_images/image_2025_11_10.jpg",
  "analysis_result": {
    "skin_health": {
      "acne": "low",
      "dark_circles": "medium",
      "wrinkles": "low",
      "hydration": "good"
    },
    "recommendations": [
      "Use moisturizer daily",
      "Get adequate sleep",
      "Stay hydrated"
    ],
    "overall_score": 7.5
  },
  "created_at": "2025-11-10T10:30:00Z"
}
```

**Error Response:** `404 Not Found`
```json
{
  "detail": "Not found."
}
```

---

## Weekly Summary Endpoints

### 8. Get Current Week Summary

**Endpoint:** `GET /api/summary/weekly/`

**Description:** Get or generate summary for current week

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "user": 1,
  "user_email": "user@example.com",
  "week_start": "2025-11-10",
  "week_end": "2025-11-16",
  "total_analyses": 5,
  "summary_data": {
    "total_scans": 5,
    "average_score": 7.2,
    "most_common_issues": {
      "medium": 3,
      "low": 2,
      "good": 4
    },
    "trend": "improving"
  },
  "created_at": "2025-11-10T10:30:00Z"
}
```

**Response (No analyses):** `200 OK`
```json
{
  "id": 1,
  "user": 1,
  "user_email": "user@example.com",
  "week_start": "2025-11-10",
  "week_end": "2025-11-16",
  "total_analyses": 0,
  "summary_data": {
    "message": "No analyses this week"
  },
  "created_at": "2025-11-10T10:30:00Z"
}
```

---

### 9. Get Summary History

**Endpoint:** `GET /api/summary/history/`

**Description:** Retrieve all weekly summaries for authenticated user

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
[
  {
    "id": 2,
    "user": 1,
    "user_email": "user@example.com",
    "week_start": "2025-11-10",
    "week_end": "2025-11-16",
    "total_analyses": 5,
    "summary_data": {
      "total_scans": 5,
      "average_score": 7.2,
      "most_common_issues": {
        "medium": 3,
        "low": 2
      },
      "trend": "improving"
    },
    "created_at": "2025-11-10T10:30:00Z"
  },
  {
    "id": 1,
    "user": 1,
    "user_email": "user@example.com",
    "week_start": "2025-11-03",
    "week_end": "2025-11-09",
    "total_analyses": 3,
    "summary_data": {
      "total_scans": 3,
      "average_score": 6.5,
      "most_common_issues": {
        "high": 2,
        "medium": 1
      },
      "trend": "needs_attention"
    },
    "created_at": "2025-11-03T10:30:00Z"
  }
]
```

---

## Authentication

All endpoints except `/api/auth/register/` and `/api/auth/login/` require JWT authentication.

Include the access token in the Authorization header:
```
Authorization: Bearer <access_token>
```

### Token Lifecycle

- **Access Token:** Valid for 1 hour
- **Refresh Token:** Valid for 7 days
- Use the refresh token to get a new access token when it expires

---

## Error Responses

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error."
}
```

---

## Testing with cURL

### Register
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","full_name":"Test User","password":"testpass123"}'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123"}'
```

### Upload Image
```bash
curl -X POST http://localhost:8000/api/analysis/ \
  -H "Authorization: Bearer <access_token>" \
  -F "image=@/path/to/image.jpg"
```

### Get Profile
```bash
curl -X GET http://localhost:8000/api/user/profile/ \
  -H "Authorization: Bearer <access_token>"
```

---

## Adding Your ML Model

To integrate your facial analysis model:

### Step 1: Add your model file
Place your trained model in the `backend/` directory (e.g., `backend/ml_model.py` or `backend/model.h5`)

### Step 2: Update the analysis view
In `backend/views.py`, replace the `_mock_facial_analysis` method:

```python
def _mock_facial_analysis(self, image_path):
    # Option 1: Import your custom model
    from .ml_model import analyze_face
    result = analyze_face(image_path)
    return result
    
    # Option 2: Use TensorFlow/Keras
    # import tensorflow as tf
    # model = tf.keras.models.load_model('backend/model.h5')
    # img = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
    # img_array = tf.keras.preprocessing.image.img_to_array(img)
    # predictions = model.predict(np.expand_dims(img_array, axis=0))
    # return process_predictions(predictions)
    
    # Option 3: Use PyTorch
    # import torch
    # from torchvision import transforms
    # from PIL import Image
    # model = torch.load('backend/model.pth')
    # image = Image.open(image_path)
    # transform = transforms.Compose([...])
    # tensor = transform(image).unsqueeze(0)
    # output = model(tensor)
    # return process_output(output)
```

### Step 3: Update the view call
In the `FacialAnalysisCreateView.post` method, pass the image path:

```python
# Change this line:
mock_result = self._mock_facial_analysis()

# To this:
mock_result = self._mock_facial_analysis(analysis.image.path)
```

### Expected Output Format
Your model should return a dictionary with this structure:

```python
{
    'skin_health': {
        'acne': 'low' | 'medium' | 'high',
        'dark_circles': 'low' | 'medium' | 'high',
        'wrinkles': 'low' | 'medium' | 'high',
        'hydration': 'poor' | 'fair' | 'good' | 'excellent'
    },
    'recommendations': [
        'Recommendation 1',
        'Recommendation 2',
        ...
    ],
    'overall_score': 7.5  # Float between 0-10
}
```

You can customize the structure based on your model's output.

---

## Database Models

### User
- `email` (unique)
- `full_name`
- `password` (hashed)
- `is_active`
- `is_staff`
- `date_joined`

### FacialAnalysis
- `user` (ForeignKey)
- `image` (ImageField)
- `analysis_result` (JSONField)
- `created_at`

### WeeklySummary
- `user` (ForeignKey)
- `week_start` (DateField)
- `week_end` (DateField)
- `total_analyses` (Integer)
- `summary_data` (JSONField)
- `created_at`

---

## Admin Panel

Access the Django admin panel at `http://localhost:8000/admin/`

Create a superuser to access:
```bash
python manage.py createsuperuser
```

---

## Next Steps

1. Add your ML model for facial analysis
2. Configure production database (PostgreSQL recommended)
3. Set up proper media storage (AWS S3, etc.)
4. Add rate limiting
5. Implement email verification
6. Add password reset functionality
7. Set up CI/CD pipeline
8. Configure production settings

---

## License

MIT
