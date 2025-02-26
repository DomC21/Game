"""
Test script for the onboarding tutorial system.
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def login():
    """Login and get access token."""
    url = f"{BASE_URL}/api/auth/login"
    data = {
        "username": "test@example.com",
        "password": "password123"
    }
    
    response = requests.post(url, data=data)
    return response.json()["access_token"]

def get_onboarding_tutorial(token):
    """Get the onboarding tutorial content."""
    url = f"{BASE_URL}/api/auth/onboarding"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(url, headers=headers)
    print(f"Onboarding Tutorial Response Status: {response.status_code}")
    
    try:
        response_json = response.json()
        print(f"Onboarding Tutorial Response Body: {json.dumps(response_json, indent=2)}")
        return response_json
    except json.JSONDecodeError:
        print(f"Onboarding Tutorial Response Body: {response.text}")
        return None

if __name__ == "__main__":
    # Login
    token = login()
    
    # Get onboarding tutorial
    tutorial = get_onboarding_tutorial(token)
    
    # Print summary
    if tutorial:
        print("\n=== Summary ===")
        print(f"Tutorial Title: {tutorial['title']}")
        print(f"Number of Steps: {len(tutorial['steps'])}")
        print(f"Is New User: {tutorial['is_new_user']}")
    else:
        print("\n=== Error ===")
        print("Failed to retrieve onboarding tutorial.")
