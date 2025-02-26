"""
Test script for the authentication system.
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_register():
    """Test user registration."""
    url = f"{BASE_URL}/api/auth/register"
    data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "password123"
    }
    
    response = requests.post(url, json=data)
    print(f"Register Response Status: {response.status_code}")
    print(f"Register Response Body: {json.dumps(response.json(), indent=2)}")
    
    return response.json()

def test_login():
    """Test user login."""
    url = f"{BASE_URL}/api/auth/login"
    data = {
        "username": "test@example.com",  # FastAPI OAuth2 uses 'username' field
        "password": "password123"
    }
    
    response = requests.post(url, data=data)  # Note: using form data, not JSON
    print(f"Login Response Status: {response.status_code}")
    print(f"Login Response Body: {json.dumps(response.json(), indent=2)}")
    
    return response.json()

def test_me(token):
    """Test getting current user profile."""
    url = f"{BASE_URL}/api/auth/me"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(url, headers=headers)
    print(f"Me Response Status: {response.status_code}")
    print(f"Me Response Body: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    # Test registration
    user = test_register()
    
    # Test login
    token_data = test_login()
    
    # Test getting user profile
    if "access_token" in token_data:
        test_me(token_data["access_token"])
