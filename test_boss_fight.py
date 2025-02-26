"""
Test script for the Boss Fight quiz functionality.
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

def get_quiz(token, quiz_id):
    """Get a quiz by ID."""
    url = f"{BASE_URL}/api/quizzes/{quiz_id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(url, headers=headers)
    print(f"Quiz {quiz_id} Response Status: {response.status_code}")
    print(f"Quiz {quiz_id} Response Body: {json.dumps(response.json(), indent=2)}")
    
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

def test_boss_fight():
    """Test the Boss Fight quiz functionality."""
    # Login
    token = login()
    
    # Get initial user profile
    print("\n=== Initial User Profile ===")
    user_before = get_user_profile(token)
    
    # Get regular quiz (Quiz 1)
    print("\n=== Regular Quiz (Quiz 1) ===")
    quiz1 = get_quiz(token, 1)
    
    # Get boss fight quiz (Quiz 2)
    print("\n=== Boss Fight Quiz (Quiz 2) ===")
    quiz2 = get_quiz(token, 2)
    
    # Prepare answers for boss fight quiz (all correct)
    boss_answers = {}
    for question in quiz2["questions"]:
        for option in question["options"]:
            if option["is_correct"]:
                boss_answers[question["id"]] = option["id"]
                break
    
    # Submit boss fight quiz with all correct answers
    print("\n=== Submit Boss Fight Quiz (All Correct) ===")
    result = submit_quiz(token, quiz2["id"], boss_answers)
    
    # Get updated user profile
    print("\n=== Updated User Profile ===")
    user_after = get_user_profile(token)
    
    # Get achievements
    print("\n=== Achievements ===")
    achievements = get_achievements(token)
    
    # Print summary
    print("\n=== Boss Fight Test Summary ===")
    print(f"Initial Points: {user_before['total_points']}")
    print(f"Updated Points: {user_after['total_points']}")
    print(f"Points Earned: {user_after['total_points'] - user_before['total_points']}")
    
    # Check if Boss Slayer achievement was earned
    boss_slayer_earned = False
    for achievement in achievements:
        if achievement["title"] == "Boss Slayer" and achievement["earned"]:
            boss_slayer_earned = True
            break
    
    print(f"Boss Slayer Achievement Earned: {boss_slayer_earned}")
    
    return {
        "points_earned": user_after['total_points'] - user_before['total_points'],
        "boss_slayer_earned": boss_slayer_earned,
        "quiz_result": result
    }

if __name__ == "__main__":
    test_results = test_boss_fight()
    
    # Verify that boss fight quiz is working correctly
    assert test_results["points_earned"] > 0, "Should earn points for completing boss fight quiz"
    assert test_results["boss_slayer_earned"], "Should earn Boss Slayer achievement"
    
    print("\n=== Boss Fight Quiz Test Passed ===")
