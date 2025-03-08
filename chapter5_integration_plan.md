# Chapter 5: Portfolio Construction & Asset Allocation - Integration Plan

## Overview
This document outlines the integration plan for Chapter 5 of the Trading Ebook application. Chapter 5 focuses on portfolio construction and asset allocation, teaching users how to build and manage investment portfolios aligned with their risk tolerance and financial goals.

## Content Structure
Chapter 5 consists of 22 subsections covering various aspects of portfolio construction and asset allocation:

1. Introduction to Portfolio Management
2. The Risk-Return Trade-Off
3. Diversification: Why It Matters
4. Core Asset Classes & Their Roles
5. Asset Allocation Strategies
6. Time Horizon & Investing Goals
7. Modern Portfolio Theory (MPT)
8. Measuring Portfolio Risk
9. Rebalancing Strategies
10. Factor Investing & Smart Beta
11. Sector & Geographic Diversification
12. Using Index Funds & ETFs
13. Bonds & Fixed Income Approaches
14. Alternative Investments
15. Portfolio Performance Metrics
16. Portfolio Drawdowns & Recovery
17. Tax Considerations
18. Example Allocations for Different Risk Profiles
19. Creating a Personal Investment Policy Statement (IPS)
20. Scenario Planning & Stress Testing
21. Putting It All Together: Sample Portfolio Construction
22. Conclusion & Next Steps

Each subsection will be stored as a markdown file in the `app/content/chapter5/` directory.

## Quiz Structure

### Subsection Mini-Quizzes
Each subsection will include 2-3 mini-quiz questions to reinforce key concepts. These questions will be embedded within the markdown content and will not be tracked in the database.

### Chapter Quiz
The chapter quiz will consist of 15 comprehensive questions covering the key concepts from all subsections. The quiz will be stored in `app/content/chapter5/chapter_quiz.md` and imported into the database using a script similar to previous chapters.

## XP Reward Structure
Chapter 5 will follow the same XP reward structure as previous chapters:

- Subsection completion: 200 XP per subsection (22 subsections × 200 XP = 4,400 XP)
- Chapter quiz completion: 100 XP
- Achievement unlocks: 125 XP per achievement (4 achievements × 125 XP = 500 XP)

Total XP available in Chapter 5: 5,000 XP

## Achievements
Chapter 5 will include the following achievements:

1. **Allocation Architect**
   - Description: Complete all 22 subsections with an 80%+ score on the quiz
   - Requirement Type: quiz_score
   - Requirement Value: 80
   - Badge Image: badge-allocation-architect.png

2. **Diversification Dynamo**
   - Description: Successfully build a sample allocation (3+ asset classes) and justify each percentage
   - Requirement Type: special_quiz_achievement
   - Requirement Value: 1
   - Badge Image: badge-diversification-dynamo.png

3. **Rebalancing Ruler**
   - Description: Demonstrate the correct process of threshold rebalancing in a scenario-based mini-quiz
   - Requirement Type: special_quiz_achievement
   - Requirement Value: 1
   - Badge Image: badge-rebalancing-ruler.png

4. **Policy Pro**
   - Description: Draft a personal Investment Policy Statement (IPS) and identify the key sections outlined in this chapter
   - Requirement Type: special_quiz_achievement
   - Requirement Value: 1
   - Badge Image: badge-policy-pro.png

## Technical Implementation

### Database Updates
1. Add Chapter 5 to the chapters table
2. Add Chapter 5 quiz to the quizzes table
3. Add Chapter 5 achievements to the achievements table
4. Create special quiz achievement requirements for the Diversification Dynamo, Rebalancing Ruler, and Policy Pro achievements

### Scripts to Create
1. `import_chapter5_quiz.py`: Import the Chapter 5 quiz questions into the database
2. `add_chapter5_achievements.py`: Add the Chapter 5 achievements to the database
3. `test_chapter5_completion.py`: Test the Chapter 5 completion flow, including quiz completion and achievement unlocks

### Frontend Updates
No significant frontend updates are required as the existing components should handle the new chapter content automatically.

## Testing Plan
1. Verify that all 22 subsections are accessible and display correctly
2. Test the Chapter 5 quiz functionality
3. Verify that XP is awarded correctly for subsection completion and quiz completion
4. Test that all achievements are unlocked correctly when their requirements are met

## Implementation Timeline
1. Create directory structure and outline files
2. Implement subsection content files
3. Create chapter quiz
4. Update database with Chapter 5 data
5. Implement achievement tracking
6. Test implementation
7. Create pull request for review

## Dependencies
- Chapter 5 implementation depends on the existing Chapter 1-4 codebase
- No new external dependencies are required
