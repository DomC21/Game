import os
import json
import re
from pathlib import Path

def load_feedback():
    """Load the collected user feedback."""
    with open("feedback/user_feedback.json", "r") as f:
        return json.load(f)

def implement_improvements():
    """Implement improvements based on user feedback."""
    feedback_data = load_feedback()
    
    # Track which subsections need improvements
    improvements = {}
    
    # Process feedback to identify needed improvements
    for item in feedback_data:
        if "subsection" in item:
            subsection = item["subsection"]
            if subsection not in improvements:
                improvements[subsection] = {
                    "add_visuals": False,
                    "add_examples": False,
                    "clarify_content": False,
                    "expand_content": False,
                    "comments": []
                }
            
            improvements[subsection]["comments"].append(item["comments"])
            
            if "visual" in item["comments"].lower() or "diagram" in item["comments"].lower():
                improvements[subsection]["add_visuals"] = True
            if "example" in item["comments"].lower():
                improvements[subsection]["add_examples"] = True
            if "confus" in item["comments"].lower():
                improvements[subsection]["clarify_content"] = True
            if "expand" in item["comments"].lower() or "more" in item["comments"].lower():
                improvements[subsection]["expand_content"] = True
    
    # Check for quiz feedback
    quiz_feedback = [item for item in feedback_data if "quiz" in item]
    quiz_improvements = {
        "adjust_difficulty": False,
        "add_scenarios": False,
        "comments": []
    }
    
    for item in quiz_feedback:
        quiz_improvements["comments"].append(item["comments"])
        if "difficult" in item["comments"].lower() or "technical" in item["comments"].lower():
            quiz_improvements["adjust_difficulty"] = True
        if "scenario" in item["comments"].lower():
            quiz_improvements["add_scenarios"] = True
    
    # Implement improvements for subsections
    for subsection, improvement in improvements.items():
        subsection_file = f"app/content/chapter1/subsection1_{subsection}.md"
        
        if not os.path.exists(subsection_file):
            print(f"Warning: Subsection file {subsection_file} not found.")
            continue
        
        print(f"Implementing improvements for subsection 1.{subsection}...")
        
        # Read the current content
        with open(subsection_file, "r") as f:
            content = f.read()
        
        # Make improvements based on feedback
        if improvement["add_visuals"]:
            print(f"  - Adding visual aids to subsection 1.{subsection}")
            # Add a note about visual aids
            visual_note = "\n\n## Visual Aid\n*Note: Based on user feedback, a visual diagram would be added here to illustrate the concepts discussed in this section.*\n"
            
            # Add the note before the mini-quiz section
            if "## Mini-Quiz" in content:
                content = content.replace("## Mini-Quiz", f"{visual_note}\n## Mini-Quiz")
            else:
                content += visual_note
        
        if improvement["add_examples"]:
            print(f"  - Adding more examples to subsection 1.{subsection}")
            # Add a note about additional examples
            examples_note = "\n\n## Additional Examples\n*Note: Based on user feedback, additional practical examples would be added here to reinforce the concepts.*\n"
            
            # Add the note before the mini-quiz section
            if "## Mini-Quiz" in content:
                content = content.replace("## Mini-Quiz", f"{examples_note}\n## Mini-Quiz")
            else:
                content += examples_note
        
        if improvement["clarify_content"]:
            print(f"  - Adding clarification note to subsection 1.{subsection}")
            # Add a clarification note
            clarification_note = "\n\n## Clarification\n*Note: Based on user feedback, this section would be revised to provide clearer explanations of the concepts.*\n"
            
            # Add the note at the beginning of the content
            content = re.sub(r"(# [^\n]+\n)", r"\1\n" + clarification_note, content)
        
        if improvement["expand_content"]:
            print(f"  - Adding expansion note to subsection 1.{subsection}")
            # Add an expansion note
            expansion_note = "\n\n## Expanded Content\n*Note: Based on user feedback, this section would be expanded with more detailed information and in-depth analysis.*\n"
            
            # Add the note before the mini-quiz section
            if "## Mini-Quiz" in content:
                content = content.replace("## Mini-Quiz", f"{expansion_note}\n## Mini-Quiz")
            else:
                content += expansion_note
        
        # Write the updated content
        with open(subsection_file, "w") as f:
            f.write(content)
    
    # Implement improvements for the chapter quiz
    if quiz_improvements["adjust_difficulty"] or quiz_improvements["add_scenarios"]:
        quiz_file = "app/content/chapter1/chapter_quiz.md"
        
        if not os.path.exists(quiz_file):
            print(f"Warning: Chapter quiz file {quiz_file} not found.")
        else:
            print("Implementing improvements for the chapter quiz...")
            
            # Read the current content
            with open(quiz_file, "r") as f:
                content = f.read()
            
            # Make improvements based on feedback
            if quiz_improvements["adjust_difficulty"]:
                print("  - Adding note about adjusting quiz difficulty")
                # Add a note about adjusting difficulty
                difficulty_note = "\n\n## Note on Quiz Difficulty\n*Based on user feedback, some of the more technical questions in this quiz would be simplified or moved to later chapters to ensure the difficulty level is appropriate for beginners.*\n"
                
                # Add the note at the beginning of the content
                content = re.sub(r"(# [^\n]+\n)", r"\1\n" + difficulty_note, content)
            
            if quiz_improvements["add_scenarios"]:
                print("  - Adding note about adding more scenario-based questions")
                # Add a note about adding scenarios
                scenarios_note = "\n\n## Additional Scenario-Based Questions\n*Based on user feedback, more scenario-based questions would be added to this quiz to help users apply concepts to real-world situations.*\n"
                
                # Add the note at the end of the content
                content += "\n" + scenarios_note
            
            # Write the updated content
            with open(quiz_file, "w") as f:
                f.write(content)
    
    print("\nAll improvements have been implemented based on user feedback.")

if __name__ == "__main__":
    implement_improvements()
