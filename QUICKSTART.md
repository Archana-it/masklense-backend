# Quick Start Guide

## ✅ Your Backend is Ready!

The server is running at: **http://localhost:8000**

---

## 🚀 Test the API

### Option 1: Use the Test Script
```bash
pip install requests pillow
python test_api.py
```

### Option 2: Use Postman
1. Import `MaskLens_API.postman_collection.json` into Postman
2. Run the requests in order (Register → Login → other endpoints)

### Option 3: Use cURL

**Register a user:**
```bash
curl -X POST http://localhost:8000/api/auth/register/ ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"test@example.com\",\"full_name\":\"Test User\",\"password\":\"testpass123\"}"
```

**Login:**
```bash
curl -X POST http://localhost:8000/api/auth/login/ ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"test@example.com\",\"password\":\"testpass123\"}"
```

**Get Profile (replace TOKEN with your access token):**
```bash
curl -X GET http://localhost:8000/api/user/profile/ ^
  -H "Authorization: Bearer TOKEN"
```

---

## 📋 Available Endpoints

### Authentication
- `POST /api/auth/register/` - Create account
- `POST /api/auth/login/` - Login
- `POST /api/auth/token/refresh/` - Refresh token

### User
- `GET /api/user/profile/` - Get profile
- `PUT/PATCH /api/user/profile/` - Update profile

### Facial Analysis
- `POST /api/analysis/` - Upload image
- `GET /api/analysis/list/` - Get all analyses
- `GET /api/analysis/<id>/` - Get single analysis

### Weekly Summary
- `GET /api/summary/weekly/` - Current week summary
- `GET /api/summary/history/` - All summaries

---

## 🤖 Add Your ML Model

### Step 1: Create your model file
```python
# backend/ml_model.py

def analyze_face(image_path):
    # Your model logic here
    # Load model, preprocess image, run inference
    
    return {
        'skin_health': {
            'acne': 'low',
            'dark_circles': 'medium',
            'wrinkles': 'low',
            'hydration': 'good'
        },
        'recommendations': ['...'],
        'overall_score': 7.5
    }
```

### Step 2: Enable it in views.py
In `backend/views.py`, uncomment these lines:
```python
from .ml_model import analyze_face
analysis_result = analyze_face(analysis.image.path)
```

See `backend/ml_model_example.py` for detailed examples!

---

## 🔧 Admin Panel

Access at: **http://localhost:8000/admin/**

Create superuser:
```bash
python manage.py createsuperuser
```

---

## 📱 Connect Your React Frontend

Your frontend should:

1. **Register/Login** to get JWT tokens
2. **Store tokens** in localStorage or state management
3. **Include token** in headers:
   ```javascript
   headers: {
     'Authorization': `Bearer ${accessToken}`
   }
   ```
4. **Upload images** as FormData:
   ```javascript
   const formData = new FormData();
   formData.append('image', imageFile);
   
   fetch('http://localhost:8000/api/analysis/', {
     method: 'POST',
     headers: {
       'Authorization': `Bearer ${accessToken}`
     },
     body: formData
   })
   ```

---

## 📚 Full Documentation

See `README.md` for complete API documentation with all request/response examples.

---

## 🐛 Troubleshooting

**Server not starting?**
- Check if port 8000 is available
- Make sure all dependencies are installed: `pip install -r requirements.txt`

**Database errors?**
- Delete `db.sqlite3` and run migrations again:
  ```bash
  del db.sqlite3
  python manage.py migrate
  ```

**CORS errors from frontend?**
- Add your frontend URL to `CORS_ALLOWED_ORIGINS` in `settings.py`

---

## 🎯 Next Steps

1. ✅ Test all endpoints
2. ✅ Add your ML model
3. ✅ Build React frontend
4. ✅ Connect frontend to backend
5. ✅ Deploy to production

Happy coding! 🚀
