import React from 'react';
import { Alert, AlertDescription, AlertTitle } from '../ui-js/alert';
import { Clock, AlertTriangle } from 'lucide-react';

const TimedQuizAlert = ({ timeLimit, onStart }) => {
  // Convert seconds to minutes and seconds
  const minutes = Math.floor(timeLimit / 60);
  const seconds = timeLimit % 60;
  
  return (
    <Alert className="mb-6 bg-orange-50 border-orange-200">
      <div className="flex items-start">
        <AlertTriangle className="h-5 w-5 text-orange-600 mr-2 mt-0.5" />
        <div>
          <AlertTitle className="text-orange-800">Timed Quiz</AlertTitle>
          <AlertDescription className="text-orange-700">
            <p>This quiz has a time limit of {minutes}:{seconds < 10 ? '0' : ''}{seconds}.</p>
            <p className="mt-1">The timer will start when you begin the quiz and you'll need to complete all questions before time runs out.</p>
          </AlertDescription>
        </div>
      </div>
    </Alert>
  );
};

export default TimedQuizAlert;
