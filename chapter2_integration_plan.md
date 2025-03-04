# Chapter 2: Integration Plan for Quizzes, XP Rewards, and Achievements

## Overview
This document outlines the plan for integrating gamification elements (quizzes, XP rewards, and achievements) into Chapter 2: "Trading Psychology & Emotional Discipline." The implementation will build upon the successful framework established in Chapter 1 while introducing new elements specific to the psychological aspects of trading.

## Quiz Integration

### Subsection Quizzes
- Each of the 22 subsections will include a mini-quiz at the end
- 3-5 questions per subsection quiz
- Question types:
  - Multiple choice
  - Scenario-based decision making
  - Self-assessment reflections
  - Emotional response identification
- Focus on application of psychological concepts rather than just recall

### Chapter Quiz
- Comprehensive assessment with 30 questions
- Mix of question types:
  - Multiple choice
  - Scenario analysis
  - Trading decision scenarios
  - Emotional response identification
  - Cognitive bias recognition
- Higher difficulty level than subsection quizzes
- Requires 80% score to earn the "Psychology Expert" achievement

## XP Reward Structure

### Subsection Quizzes
- Base XP: 75-100 XP per subsection quiz
- Total from all subsection quizzes: ~1,800-2,200 XP

### Chapter Quiz
- Base completion: 1,000 XP
- "Psychology Expert" achievement bonus: 2,000 XP
- Total possible from Chapter Quiz: 3,000 XP

### Total Chapter 2 XP
- Approximately 4,800-5,200 XP (consistent with Chapter 1)
- Contributes significantly toward Level 2 (1,000 XP) and Level 3 (5,000 XP) thresholds

## Achievement Integration

### Chapter-Specific Achievement
- **Psychology Expert**
  - Description: Complete all subsections in Chapter 2 and score at least 80% on the chapter quiz
  - Badge: badge-psychology-expert.png
  - Requirement Type: quiz_score
  - Requirement Value: 80
  - Chapter ID: 2

### Additional Achievements
- **Emotional Mastery**
  - Description: Complete the emotional self-assessment exercises in all subsections
  - Badge: badge-emotional-mastery.png
  - Requirement Type: subsection_completion
  - Requirement Value: 22
  - Chapter ID: 2

- **Bias Buster**
  - Description: Correctly identify all cognitive biases in the Chapter 2 quiz
  - Badge: badge-bias-buster.png
  - Requirement Type: special_quiz_achievement
  - Requirement Value: 1
  - Chapter ID: 2

## Technical Implementation

### Database Updates
- Add new achievements to the Achievement table
- Create content files for all 22 subsections
- Update seed_data.py to include Chapter 2 quiz questions

### Backend Logic
- Extend existing quiz processing logic to handle new achievement types
- Implement special tracking for the "Bias Buster" achievement
- Ensure proper XP allocation for all Chapter 2 activities

### Frontend Updates
- Create UI components for displaying psychological concepts
- Add self-assessment components for emotional exercises
- Update achievement display to include new Chapter 2 badges

## Testing Plan
- Verify all subsection quizzes award correct XP
- Test Chapter 2 quiz scoring and achievement awarding
- Validate that XP contributes correctly to level progression
- Ensure all new achievements trigger appropriately

## Integration with Chapter 1
- Maintain consistent XP scaling between chapters
- Ensure achievements from both chapters display properly in user profiles
- Verify that level progression works seamlessly across chapters
