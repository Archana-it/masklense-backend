"""
Quick API Test Script
Run this to test all endpoints after starting the server
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_register():
    print("\n=== Testing Registration ===")
    data = {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "testpass123"
    }
    response = requests.post(f"{BASE_URL}/auth/register/", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()

def test_login():
    print("\n=== Testing Login ===")
    data = {
        "email": "test@example.com",
        "password": "testpass123"
    }
    response = requests.post(f"{BASE_URL}/auth/login/", json=data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    return result.get('tokens', {}).get('access')

def test_profile(token):
    print("\n=== Testing Profile ===")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/user/profile/", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_upload_image(token):
    print("\n=== Testing Image Upload ===")
    headers = {"Authorization": f"Bearer {token}"}
    # Create a dummy image file
    from io import BytesIO
    from PIL import Image
    
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    files = {'image': ('test.jpg', img_bytes, 'image/jpeg')}
    response = requests.post(f"{BASE_URL}/analysis/", headers=headers, files=files)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_analysis_list(token):
    print("\n=== Testing Analysis List ===")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/analysis/list/", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_weekly_summary(token):
    print("\n=== Testing Weekly Summary ===")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/summary/weekly/", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    print("Starting API Tests...")
    print("Make sure the server is running: python manage.py runserver")
    
    try:
        # Register
        test_register()
        
        # Login
        token = test_login()
        
        if token:
            # Test authenticated endpoints
            test_profile(token)
            test_upload_image(token)
            test_analysis_list(token)
            test_weekly_summary(token)
            
            print("\n✅ All tests completed!")
        else:
            print("\n❌ Failed to get access token")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
