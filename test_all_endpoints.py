"""
Comprehensive test script for all backend endpoints.
This script tests the entire functionality of the trading eBook application.
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint."""
    url = f"{BASE_URL}/healthz"
    response = requests.get(url)
    print(f"Health Check Response Status: {response.status_code}")
    print(f"Health Check Response Body: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200, "Health check should return 200 OK"
    assert response.json()["status"] == "ok", "Health check should return status: ok"
    
    return True

def test_registration_and_login():
    """Test user registration and login."""
    # Test registration with a unique email
    import time
    timestamp = int(time.time())
    register_url = f"{BASE_URL}/api/auth/register"
    register_data = {
        "email": f"newuser{timestamp}@example.com",
        "username": f"newuser{timestamp}",
        "password": "password123"
    }
    
    register_response = requests.post(register_url, json=register_data)
    print(f"Register Response Status: {register_response.status_code}")
    print(f"Register Response Body: {json.dumps(register_response.json(), indent=2)}")
    
    assert register_response.status_code == 200, "Registration should succeed"
    assert register_response.json()["email"] == register_data["email"], "Registration should return correct email"
    assert register_response.json()["username"] == register_data["username"], "Registration should return correct username"
    
    # Test login
    login_url = f"{BASE_URL}/api/auth/login"
    login_data = {
        "username": register_data["email"],
        "password": register_data["password"]
    }
    
    login_response = requests.post(login_url, data=login_data)
    print(f"Login Response Status: {login_response.status_code}")
    print(f"Login Response Body: {json.dumps(login_response.json(), indent=2)}")
    
    assert login_response.status_code == 200, "Login should succeed"
    assert "access_token" in login_response.json(), "Login should return access token"
    
    token = login_response.json()["access_token"]
    
    # Test user profile
    profile_url = f"{BASE_URL}/api/auth/me"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    profile_response = requests.get(profile_url, headers=headers)
    print(f"Profile Response Status: {profile_response.status_code}")
    print(f"Profile Response Body: {json.dumps(profile_response.json(), indent=2)}")
    
    assert profile_response.status_code == 200, "Profile retrieval should succeed"
    assert profile_response.json()["email"] == register_data["email"], "Profile should have correct email"
    assert profile_response.json()["username"] == register_data["username"], "Profile should have correct username"
    
    # Test onboarding tutorial
    onboarding_url = f"{BASE_URL}/api/auth/onboarding"
    onboarding_response = requests.get(onboarding_url, headers=headers)
    print(f"Onboarding Response Status: {onboarding_response.status_code}")
    print(f"Onboarding Response Body: {json.dumps(onboarding_response.json(), indent=2)}")
    
    assert onboarding_response.status_code == 200, "Onboarding retrieval should succeed"
    assert "steps" in onboarding_response.json(), "Onboarding should include steps"
    assert onboarding_response.json()["is_new_user"] == True, "New user should be marked as new"
    
    return token

def test_content_access(token):
    """Test access to content endpoints."""
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Test levels endpoint
    levels_url = f"{BASE_URL}/api/levels"
    levels_response = requests.get(levels_url, headers=headers)
    print(f"Levels Response Status: {levels_response.status_code}")
    print(f"Levels Response Body: {json.dumps(levels_response.json(), indent=2)}")
    
    assert levels_response.status_code == 200, "Levels retrieval should succeed"
    assert len(levels_response.json()) > 0, "Should return at least one level"
    
    # Get first level
    level_id = levels_response.json()[0]["id"]
    
    # Test level details endpoint
    level_url = f"{BASE_URL}/api/levels/{level_id}"
    level_response = requests.get(level_url, headers=headers)
    print(f"Level {level_id} Response Status: {level_response.status_code}")
    print(f"Level {level_id} Response Body: {json.dumps(level_response.json(), indent=2)}")
    
    assert level_response.status_code == 200, "Level details retrieval should succeed"
    assert "chapters" in level_response.json(), "Level details should include chapters"
    
    # Get first chapter
    chapter_id = level_response.json()["chapters"][0]["id"]
    
    # Test chapter details endpoint
    chapter_url = f"{BASE_URL}/api/chapters/{chapter_id}"
    chapter_response = requests.get(chapter_url, headers=headers)
    print(f"Chapter {chapter_id} Response Status: {chapter_response.status_code}")
    print(f"Chapter {chapter_id} Response Body: {json.dumps(chapter_response.json(), indent=2)}")
    
    assert chapter_response.status_code == 200, "Chapter details retrieval should succeed"
    assert "quizzes" in chapter_response.json(), "Chapter details should include quizzes"
    
    # Get first quiz
    quiz_id = chapter_response.json()["quizzes"][0]["id"]
    
    # Test quiz details endpoint
    quiz_url = f"{BASE_URL}/api/quizzes/{quiz_id}"
    quiz_response = requests.get(quiz_url, headers=headers)
    print(f"Quiz {quiz_id} Response Status: {quiz_response.status_code}")
    print(f"Quiz {quiz_id} Response Body: {json.dumps(quiz_response.json(), indent=2)}")
    
    assert quiz_response.status_code == 200, "Quiz details retrieval should succeed"
    assert "questions" in quiz_response.json(), "Quiz details should include questions"
    
    return {
        "level_id": level_id,
        "chapter_id": chapter_id,
        "quiz_id": quiz_id,
        "quiz": quiz_response.json()
    }

def test_quiz_submission(token, quiz_data):
    """Test quiz submission and scoring."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Get user profile before quiz
    profile_url = f"{BASE_URL}/api/auth/me"
    profile_before = requests.get(profile_url, headers=headers).json()
    print(f"Profile Before Quiz - Points: {profile_before['total_points']}, Level: {profile_before['current_level']}")
    
    # Prepare answers (all correct)
    quiz = quiz_data["quiz"]
    answers = {}
    for question in quiz["questions"]:
        for option in question["options"]:
            if option["is_correct"]:
                answers[question["id"]] = option["id"]
                break
    
    # Submit quiz
    submit_url = f"{BASE_URL}/api/quizzes/{quiz['id']}/submit"
    submit_data = {
        "quiz_id": quiz["id"],
        "answers": answers
    }
    
    submit_response = requests.post(submit_url, headers=headers, json=submit_data)
    print(f"Quiz Submission Response Status: {submit_response.status_code}")
    print(f"Quiz Submission Response Body: {json.dumps(submit_response.json(), indent=2)}")
    
    assert submit_response.status_code == 200, "Quiz submission should succeed"
    assert "score" in submit_response.json(), "Quiz result should include score"
    assert "points_earned" in submit_response.json(), "Quiz result should include points earned"
    
    # Get user profile after quiz
    profile_after = requests.get(profile_url, headers=headers).json()
    print(f"Profile After Quiz - Points: {profile_after['total_points']}, Level: {profile_after['current_level']}")
    
    # Verify points were awarded
    points_earned = profile_after["total_points"] - profile_before["total_points"]
    assert points_earned > 0, "User should earn points from quiz"
    assert points_earned == submit_response.json()["points_earned"], "Points earned should match quiz result"
    
    # Check quiz attempts
    attempts_url = f"{BASE_URL}/api/users/quiz-attempts"
    attempts_response = requests.get(attempts_url, headers=headers)
    print(f"Quiz Attempts Response Status: {attempts_response.status_code}")
    print(f"Quiz Attempts Response Body: {json.dumps(attempts_response.json(), indent=2)}")
    
    assert attempts_response.status_code == 200, "Quiz attempts retrieval should succeed"
    assert len(attempts_response.json()) > 0, "Should have at least one quiz attempt"
    
    return {
        "points_earned": points_earned,
        "profile_before": profile_before,
        "profile_after": profile_after
    }

def test_progress_tracking(token, level_id):
    """Test progress tracking."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Get initial progress
    progress_url = f"{BASE_URL}/api/users/progress"
    progress_before = requests.get(progress_url, headers=headers).json()
    print(f"Progress Before Update: {json.dumps(progress_before, indent=2)}")
    
    # Update progress for level
    update_url = f"{BASE_URL}/api/users/progress/{level_id}"
    update_data = {
        "level_id": level_id,
        "is_completed": True
    }
    
    update_response = requests.put(update_url, headers=headers, json=update_data)
    print(f"Progress Update Response Status: {update_response.status_code}")
    print(f"Progress Update Response Body: {json.dumps(update_response.json(), indent=2)}")
    
    assert update_response.status_code == 200, "Progress update should succeed"
    assert update_response.json()["is_completed"] == True, "Level should be marked as completed"
    
    # Get updated progress
    progress_after = requests.get(progress_url, headers=headers).json()
    print(f"Progress After Update: {json.dumps(progress_after, indent=2)}")
    
    # Verify level was marked as completed
    level_completed = False
    for progress in progress_after:
        if progress["level_id"] == level_id and progress["is_completed"]:
            level_completed = True
            break
    
    assert level_completed, f"Level {level_id} should be marked as completed"
    
    return {
        "progress_before": progress_before,
        "progress_after": progress_after,
        "level_completed": level_completed
    }

def test_achievements(token):
    """Test achievements system."""
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Get user achievements
    user_achievements_url = f"{BASE_URL}/api/users/achievements"
    user_achievements_response = requests.get(user_achievements_url, headers=headers)
    print(f"User Achievements Response Status: {user_achievements_response.status_code}")
    print(f"User Achievements Response Body: {json.dumps(user_achievements_response.json(), indent=2)}")
    
    assert user_achievements_response.status_code == 200, "User achievements retrieval should succeed"
    
    # Get all achievements with earned status
    all_achievements_url = f"{BASE_URL}/api/achievements"
    all_achievements_response = requests.get(all_achievements_url, headers=headers)
    print(f"All Achievements Response Status: {all_achievements_response.status_code}")
    print(f"All Achievements Response Body: {json.dumps(all_achievements_response.json(), indent=2)}")
    
    assert all_achievements_response.status_code == 200, "All achievements retrieval should succeed"
    
    # Verify at least one achievement was earned
    earned_achievements = [a for a in all_achievements_response.json() if a["earned"]]
    assert len(earned_achievements) > 0, "User should have earned at least one achievement"
    
    return {
        "user_achievements": user_achievements_response.json(),
        "all_achievements": all_achievements_response.json(),
        "earned_count": len(earned_achievements)
    }

def test_leaderboard():
    """Test leaderboard functionality."""
    leaderboard_url = f"{BASE_URL}/api/leaderboard"
    leaderboard_response = requests.get(leaderboard_url)
    print(f"Leaderboard Response Status: {leaderboard_response.status_code}")
    print(f"Leaderboard Response Body: {json.dumps(leaderboard_response.json(), indent=2)}")
    
    assert leaderboard_response.status_code == 200, "Leaderboard retrieval should succeed"
    assert len(leaderboard_response.json()) > 0, "Leaderboard should have at least one entry"
    
    return leaderboard_response.json()

def run_all_tests():
    """Run all tests in sequence."""
    print("\n=== STARTING COMPREHENSIVE BACKEND TESTS ===\n")
    
    print("\n=== 1. HEALTH CHECK TEST ===\n")
    health_check_result = test_health_check()
    
    print("\n=== 2. REGISTRATION AND LOGIN TEST ===\n")
    token = test_registration_and_login()
    
    print("\n=== 3. CONTENT ACCESS TEST ===\n")
    content_data = test_content_access(token)
    
    print("\n=== 4. QUIZ SUBMISSION TEST ===\n")
    quiz_result = test_quiz_submission(token, content_data)
    
    print("\n=== 5. PROGRESS TRACKING TEST ===\n")
    progress_result = test_progress_tracking(token, content_data["level_id"])
    
    print("\n=== 6. ACHIEVEMENTS TEST ===\n")
    achievements_result = test_achievements(token)
    
    print("\n=== 7. LEADERBOARD TEST ===\n")
    leaderboard_result = test_leaderboard()
    
    print("\n=== TEST SUMMARY ===\n")
    print("✅ Health Check: Success")
    print(f"✅ Registration and Login: Success (Token received)")
    print(f"✅ Content Access: Success (Accessed level {content_data['level_id']}, chapter {content_data['chapter_id']}, quiz {content_data['quiz_id']})")
    print(f"✅ Quiz Submission: Success (Earned {quiz_result['points_earned']} points)")
    print(f"✅ Progress Tracking: Success (Level {content_data['level_id']} completed: {progress_result['level_completed']})")
    print(f"✅ Achievements: Success (Earned {achievements_result['earned_count']} achievements)")
    print(f"✅ Leaderboard: Success ({len(leaderboard_result)} entries)")
    
    print("\n=== ALL TESTS PASSED SUCCESSFULLY ===\n")
    
    return {
        "health_check": health_check_result,
        "token": token,
        "content_data": content_data,
        "quiz_result": quiz_result,
        "progress_result": progress_result,
        "achievements_result": achievements_result,
        "leaderboard_result": leaderboard_result
    }

if __name__ == "__main__":
    run_all_tests()
