"""
Test script for the progress tracking system.
"""
import requests
import json
import time

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

def get_levels(token):
    """Get all levels with locked/unlocked status."""
    url = f"{BASE_URL}/api/levels"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(url, headers=headers)
    print(f"Levels Response Status: {response.status_code}")
    print(f"Levels Response Body: {json.dumps(response.json(), indent=2)}")
    
    return response.json()

def get_level_details(token, level_id):
    """Get details of a specific level with its chapters."""
    url = f"{BASE_URL}/api/levels/{level_id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(url, headers=headers)
    print(f"Level {level_id} Response Status: {response.status_code}")
    print(f"Level {level_id} Response Body: {json.dumps(response.json(), indent=2)}")
    
    return response.json()

def get_user_progress(token):
    """Get the user's progress across all levels."""
    url = f"{BASE_URL}/api/users/progress"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(url, headers=headers)
    print(f"User Progress Response Status: {response.status_code}")
    print(f"User Progress Response Body: {json.dumps(response.json(), indent=2)}")
    
    return response.json()

def update_user_progress(token, level_id, is_completed=True):
    """Update the user's progress for a specific level."""
    url = f"{BASE_URL}/api/users/progress/{level_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "level_id": level_id,
        "is_completed": is_completed
    }
    
    response = requests.put(url, headers=headers, json=data)
    print(f"Update Progress Response Status: {response.status_code}")
    print(f"Update Progress Response Body: {json.dumps(response.json(), indent=2)}")
    
    return response.json()

def get_user_achievements(token):
    """Get the user's earned achievements."""
    url = f"{BASE_URL}/api/users/achievements"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(url, headers=headers)
    print(f"User Achievements Response Status: {response.status_code}")
    print(f"User Achievements Response Body: {json.dumps(response.json(), indent=2)}")
    
    return response.json()

def get_all_achievements(token):
    """Get all achievements with earned status."""
    url = f"{BASE_URL}/api/achievements"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(url, headers=headers)
    print(f"All Achievements Response Status: {response.status_code}")
    print(f"All Achievements Response Body: {json.dumps(response.json(), indent=2)}")
    
    return response.json()

def get_quiz_attempts(token, quiz_id=None):
    """Get the user's quiz attempts."""
    url = f"{BASE_URL}/api/users/quiz-attempts"
    if quiz_id:
        url += f"?quiz_id={quiz_id}"
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(url, headers=headers)
    print(f"Quiz Attempts Response Status: {response.status_code}")
    print(f"Quiz Attempts Response Body: {json.dumps(response.json(), indent=2)}")
    
    return response.json()

def test_progress_tracking():
    """Test the progress tracking system."""
    # Login
    token = login()
    
    # Get initial user profile
    print("\n=== Initial User Profile ===")
    user_before = get_user_profile(token)
    
    # Get all levels
    print("\n=== All Levels ===")
    levels = get_levels(token)
    
    # Get level 1 details
    print("\n=== Level 1 Details ===")
    level1 = get_level_details(token, 1)
    
    # Get initial user progress
    print("\n=== Initial User Progress ===")
    progress_before = get_user_progress(token)
    
    # Update progress for level 1 (mark as completed)
    print("\n=== Update Progress for Level 1 ===")
    updated_progress = update_user_progress(token, 1, True)
    
    # Get updated user progress
    print("\n=== Updated User Progress ===")
    progress_after = get_user_progress(token)
    
    # Get user achievements
    print("\n=== User Achievements ===")
    user_achievements = get_user_achievements(token)
    
    # Get all achievements
    print("\n=== All Achievements ===")
    all_achievements = get_all_achievements(token)
    
    # Get quiz attempts
    print("\n=== Quiz Attempts ===")
    quiz_attempts = get_quiz_attempts(token)
    
    # Get updated user profile
    print("\n=== Updated User Profile ===")
    user_after = get_user_profile(token)
    
    # Print summary
    print("\n=== Progress Tracking Summary ===")
    print(f"Initial Level: {user_before['current_level']}")
    print(f"Initial Points: {user_before['total_points']}")
    print(f"Initial XP: {user_before['experience_points']}")
    
    print(f"Updated Level: {user_after['current_level']}")
    print(f"Updated Points: {user_after['total_points']}")
    print(f"Updated XP: {user_after['experience_points']}")
    
    # Check if level 1 is marked as completed
    level1_completed = False
    for progress in progress_after:
        if progress['level_id'] == 1 and progress['is_completed']:
            level1_completed = True
            break
    
    print(f"Level 1 Completed: {level1_completed}")
    
    # Check if any achievements were earned
    print(f"Achievements Earned: {len(user_achievements)}")
    
    return {
        "user_before": user_before,
        "user_after": user_after,
        "progress_before": progress_before,
        "progress_after": progress_after,
        "level1_completed": level1_completed,
        "achievements_earned": len(user_achievements)
    }

if __name__ == "__main__":
    test_results = test_progress_tracking()
    
    # Verify that progress tracking is working correctly
    assert test_results["level1_completed"] == True, "Level 1 should be marked as completed"
    
    print("\n=== Progress Tracking Test Passed ===")
