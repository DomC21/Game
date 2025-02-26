import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui-js/card';
import { Badge } from '../ui-js/badge';

const QuizHistoryCard = ({ quizAttempts }) => {
  // Sort quiz attempts by date (newest first)
  const sortedAttempts = [...quizAttempts].sort((a, b) => 
    new Date(b.completed_at) - new Date(a.completed_at)
  );
  
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center">
          <span className="text-purple-500 mr-2">📝</span>
          Quiz History
        </CardTitle>
      </CardHeader>
      <CardContent>
        {sortedAttempts.length > 0 ? (
          <div className="space-y-4">
            {sortedAttempts.map((attempt) => (
              <QuizAttemptItem key={attempt.id} attempt={attempt} />
            ))}
          </div>
        ) : (
          <div className="text-center py-6 text-gray-500">
            You haven't taken any quizzes yet.
          </div>
        )}
      </CardContent>
    </Card>
  );
};

const QuizAttemptItem = ({ attempt }) => {
  const { 
    quiz_title, 
    score, 
    max_score, 
    completed_at, 
    points_earned, 
    is_passed 
  } = attempt;
  
  const scorePercentage = Math.round((score / max_score) * 100);
  
  // Determine badge color based on score
  let badgeVariant = 'default';
  if (scorePercentage >= 90) {
    badgeVariant = 'success';
  } else if (scorePercentage >= 70) {
    badgeVariant = 'info';
  } else if (scorePercentage >= 50) {
    badgeVariant = 'warning';
  } else {
    badgeVariant = 'error';
  }
  
  return (
    <div className="border rounded-lg p-3 bg-white">
      <div className="flex justify-between items-start">
        <div>
          <h4 className="font-medium text-gray-800">{quiz_title}</h4>
          <p className="text-xs text-gray-500 mt-1">
            Completed on {new Date(completed_at).toLocaleDateString()}
          </p>
        </div>
        <Badge 
          className={`${
            is_passed 
              ? 'bg-green-100 text-green-800' 
              : 'bg-red-100 text-red-800'
          }`}
        >
          {is_passed ? 'Passed' : 'Failed'}
        </Badge>
      </div>
      
      <div className="mt-3 flex items-center justify-between">
        <div className="flex items-center">
          <div className="w-10 h-10 rounded-full flex items-center justify-center mr-2 text-sm font-medium bg-gray-100">
            {scorePercentage}%
          </div>
          <div className="text-sm">
            <div>Score: {score}/{max_score}</div>
            <div className="text-green-600 font-medium">+{points_earned} points</div>
          </div>
        </div>
        
        <div className="text-xs px-2 py-1 rounded bg-gray-100 text-gray-600">
          {getScoreLabel(scorePercentage)}
        </div>
      </div>
    </div>
  );
};

// Helper function to get score label
const getScoreLabel = (percentage) => {
  if (percentage >= 90) return 'Excellent';
  if (percentage >= 80) return 'Great';
  if (percentage >= 70) return 'Good';
  if (percentage >= 60) return 'Satisfactory';
  if (percentage >= 50) return 'Needs Improvement';
  return 'Try Again';
};

export default QuizHistoryCard;
