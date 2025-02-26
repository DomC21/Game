import json
import os
from datetime import datetime

def collect_feedback():
    """
    Simulated feedback collection from test users.
    In a real application, this would be an API endpoint or form submission.
    """
    # Simulated feedback from test users
    feedback_data = [
        {
            "user_id": "test_user_1",
            "timestamp": datetime.now().isoformat(),
            "chapter": 1,
            "subsection": 3,
            "clarity_rating": 4,
            "difficulty_rating": 3,
            "engagement_rating": 4,
            "comments": "The time horizon section is good, but could use more visual aids to explain the glide path concept."
        },
        {
            "user_id": "test_user_2",
            "timestamp": datetime.now().isoformat(),
            "chapter": 1,
            "subsection": 7,
            "clarity_rating": 3,
            "difficulty_rating": 4,
            "engagement_rating": 3,
            "comments": "The risk tolerance assessment was a bit confusing. Maybe add more examples of how different risk profiles might approach the same investment scenario."
        },
        {
            "user_id": "test_user_3",
            "timestamp": datetime.now().isoformat(),
            "chapter": 1,
            "subsection": 12,
            "clarity_rating": 5,
            "difficulty_rating": 2,
            "engagement_rating": 4,
            "comments": "The compound interest examples were great, but I'd like to see more interactive calculators or tools to experiment with different scenarios."
        },
        {
            "user_id": "test_user_4",
            "timestamp": datetime.now().isoformat(),
            "chapter": 1,
            "subsection": 15,
            "clarity_rating": 4,
            "difficulty_rating": 3,
            "engagement_rating": 3,
            "comments": "The section on ETFs vs. mutual funds could be expanded with a clearer comparison table."
        },
        {
            "user_id": "test_user_5",
            "timestamp": datetime.now().isoformat(),
            "chapter": 1,
            "subsection": 20,
            "clarity_rating": 4,
            "difficulty_rating": 4,
            "engagement_rating": 5,
            "comments": "The global investing section was informative but could benefit from more specific examples of international diversification strategies."
        },
        {
            "user_id": "test_user_6",
            "timestamp": datetime.now().isoformat(),
            "chapter": 1,
            "quiz": "chapter_quiz",
            "clarity_rating": 4,
            "difficulty_rating": 4,
            "engagement_rating": 4,
            "comments": "The chapter quiz was comprehensive, but some questions felt too technical for an introductory chapter. Consider adding more scenario-based questions."
        }
    ]
    
    # Save feedback to a JSON file
    with open("feedback/user_feedback.json", "w") as f:
        json.dump(feedback_data, f, indent=2)
    
    print(f"Collected feedback from {len(feedback_data)} test users.")
    return feedback_data

def analyze_feedback(feedback_data):
    """
    Analyze feedback to identify areas for improvement.
    """
    print("\nFeedback Analysis:")
    print("-----------------")
    
    # Calculate average ratings
    clarity_sum = sum(item["clarity_rating"] for item in feedback_data)
    difficulty_sum = sum(item["difficulty_rating"] for item in feedback_data)
    engagement_sum = sum(item["engagement_rating"] for item in feedback_data)
    
    avg_clarity = clarity_sum / len(feedback_data)
    avg_difficulty = difficulty_sum / len(feedback_data)
    avg_engagement = engagement_sum / len(feedback_data)
    
    print(f"Average Clarity Rating: {avg_clarity:.2f}/5")
    print(f"Average Difficulty Rating: {avg_difficulty:.2f}/5")
    print(f"Average Engagement Rating: {avg_engagement:.2f}/5")
    
    # Identify subsections with feedback
    subsections_with_feedback = {}
    for item in feedback_data:
        if "subsection" in item:
            subsection = item["subsection"]
            if subsection not in subsections_with_feedback:
                subsections_with_feedback[subsection] = []
            subsections_with_feedback[subsection].append(item)
    
    print("\nSubsections with Feedback:")
    for subsection, items in subsections_with_feedback.items():
        print(f"\nSubsection {subsection}:")
        for item in items:
            print(f"  - {item['comments']}")
    
    # Check for quiz feedback
    quiz_feedback = [item for item in feedback_data if "quiz" in item]
    if quiz_feedback:
        print("\nQuiz Feedback:")
        for item in quiz_feedback:
            print(f"  - {item['comments']}")
    
    # Generate improvement recommendations
    print("\nImprovement Recommendations:")
    
    # Subsection improvements
    for subsection, items in subsections_with_feedback.items():
        for item in items:
            if "visual" in item["comments"].lower() or "diagram" in item["comments"].lower():
                print(f"  - Add more visual aids to subsection {subsection}")
            if "example" in item["comments"].lower():
                print(f"  - Add more examples to subsection {subsection}")
            if "confus" in item["comments"].lower():
                print(f"  - Clarify content in subsection {subsection}")
            if "expand" in item["comments"].lower() or "more" in item["comments"].lower():
                print(f"  - Expand content in subsection {subsection}")
    
    # Quiz improvements
    for item in quiz_feedback:
        if "difficult" in item["comments"].lower() or "technical" in item["comments"].lower():
            print("  - Adjust quiz difficulty to be more appropriate for beginners")
        if "scenario" in item["comments"].lower():
            print("  - Add more scenario-based questions to the quiz")
    
    return {
        "avg_clarity": avg_clarity,
        "avg_difficulty": avg_difficulty,
        "avg_engagement": avg_engagement,
        "subsections_with_feedback": subsections_with_feedback,
        "quiz_feedback": quiz_feedback
    }

if __name__ == "__main__":
    feedback_data = collect_feedback()
    analysis = analyze_feedback(feedback_data)
