"""
Test script for quiz submission and gamification features.
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

def get_quiz(token, quiz_id=1):
    """Get a quiz by ID."""
    url = f"{BASE_URL}/api/quizzes/{quiz_id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(url, headers=headers)
    print(f"Quiz Response Status: {response.status_code}")
    print(f"Quiz Response Body: {json.dumps(response.json(), indent=2)}")
    
    return response.json()

def submit_quiz(token, quiz_id, answers):
    """Submit answers for a quiz."""
    url = f"{BASE_URL}/api/quizzes/{quiz_id}/submit"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "quiz_id": quiz_id,
        "answers": answers
    }
    
    response = requests.post(url, headers=headers, json=data)
    print(f"Submit Quiz Response Status: {response.status_code}")
    
    try:
        response_json = response.json()
        print(f"Submit Quiz Response Body: {json.dumps(response_json, indent=2)}")
        return response_json
    except json.JSONDecodeError:
        print(f"Submit Quiz Response Body: {response.text}")
        return None

def get_user_profile(token):
    """Get the user's profile with gamification data."""
    url = f"{BASE_URL}/api/auth/me"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(url, headers=headers)
    print(f"User Profile Response Status: {response.status_code}")
    print(f"User Profile Response Body: {json.dumps(response.json(), indent=2)}")
    
    return response.json()

def get_achievements(token):
    """Get all achievements with earned status."""
    url = f"{BASE_URL}/api/achievements"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(url, headers=headers)
    print(f"Achievements Response Status: {response.status_code}")
    print(f"Achievements Response Body: {json.dumps(response.json(), indent=2)}")
    
    return response.json()

def get_leaderboard():
    """Get the leaderboard."""
    url = f"{BASE_URL}/api/leaderboard"
    
    response = requests.get(url)
    print(f"Leaderboard Response Status: {response.status_code}")
    print(f"Leaderboard Response Body: {json.dumps(response.json(), indent=2)}")
    
    return response.json()

if __name__ == "__main__":
    # Login
    token = login()
    
    # Get user profile before quiz
    print("\n=== User Profile Before Quiz ===")
    user_before = get_user_profile(token)
    
    # Get quiz
    print("\n=== Quiz Details ===")
    quiz = get_quiz(token)
    
    # Check if quiz has questions
    if not quiz["questions"]:
        print("\nQuiz has no questions. Skipping quiz submission test.")
    else:
        # Prepare answers (all correct for testing)
        answers = {}
        for question in quiz["questions"]:
            for option in question["options"]:
                if option["is_correct"]:
                    answers[question["id"]] = option["id"]
                    break
        
        # Submit quiz
        print("\n=== Quiz Submission ===")
        result = submit_quiz(token, quiz["id"], answers)
        
        # Get user profile after quiz
        print("\n=== User Profile After Quiz ===")
        user_after = get_user_profile(token)
        
        # Get achievements
        print("\n=== Achievements ===")
        achievements = get_achievements(token)
        
        # Get leaderboard
        print("\n=== Leaderboard ===")
        leaderboard = get_leaderboard()
        
        # Print summary
        print("\n=== Summary ===")
        print(f"Points before quiz: {user_before['total_points']}")
        print(f"Points after quiz: {user_after['total_points']}")
        print(f"Points earned: {user_after['total_points'] - user_before['total_points']}")
        print(f"Level before quiz: {user_before['current_level']}")
        print(f"Level after quiz: {user_after['current_level']}")
