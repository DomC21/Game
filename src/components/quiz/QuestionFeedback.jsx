import React from 'react';
import { Alert, AlertDescription, AlertTitle } from '../ui-js/alert';
import { CheckCircle, XCircle, Info } from 'lucide-react';

const QuestionFeedback = ({ isCorrect, explanation, points }) => {
  return (
    <Alert className={`mb-4 ${isCorrect ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'}`}>
      <div className="flex items-start">
        {isCorrect ? (
          <CheckCircle className="h-5 w-5 text-green-600 mr-2 mt-0.5" />
        ) : (
          <XCircle className="h-5 w-5 text-red-600 mr-2 mt-0.5" />
        )}
        <div>
          <AlertTitle className={isCorrect ? 'text-green-800' : 'text-red-800'}>
            {isCorrect ? 'Correct!' : 'Incorrect'}
            {points && isCorrect && <span className="ml-2">+{points} points</span>}
          </AlertTitle>
          <AlertDescription className="text-gray-700">
            {explanation}
          </AlertDescription>
        </div>
      </div>
    </Alert>
  );
};

export default QuestionFeedback;
