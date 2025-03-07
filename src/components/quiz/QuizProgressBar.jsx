import React from 'react';
import { Progress } from '../ui-js/progress';

const QuizProgressBar = ({ currentQuestion, totalQuestions, answeredQuestions }) => {
  // Calculate progress percentage
  const progress = ((currentQuestion + 1) / totalQuestions) * 100;
  
  // Calculate completion percentage
  const completionPercentage = (answeredQuestions / totalQuestions) * 100;
  
  return (
    <div className="space-y-2">
      <div className="flex justify-between text-sm text-gray-500">
        <span>Question {currentQuestion + 1} of {totalQuestions}</span>
        <span>{Math.round(completionPercentage)}% Complete</span>
      </div>
      <Progress value={progress} className="h-2" />
      <div className="flex justify-between text-xs text-gray-400">
        <span>Start</span>
        <span>Finish</span>
      </div>
    </div>
  );
};

export default QuizProgressBar;
