import React, { useState } from 'react';
import { Button } from '../ui-js/button';
import { Card, CardContent } from '../ui-js/card';

const PatternRecognition = ({ pattern, options, correctAnswer, onAnswer }) => {
  const [selectedOption, setSelectedOption] = useState(null);
  const [showFeedback, setShowFeedback] = useState(false);
  
  const handleOptionSelect = (option) => {
    setSelectedOption(option);
  };
  
  const handleSubmit = () => {
    setShowFeedback(true);
    onAnswer(selectedOption === correctAnswer);
  };
  
  return (
    <div className="space-y-4">
      <div className="bg-white p-4 rounded-lg border border-gray-200">
        <h3 className="font-medium text-lg mb-4">Identify the Pattern</h3>
        
        <div className="flex justify-center mb-6">
          {/* Display the pattern - could be images, chart, or text */}
          <div className="p-4 bg-gray-50 rounded-lg border border-gray-200 w-full">
            {typeof pattern === 'string' ? (
              <p className="text-center">{pattern}</p>
            ) : (
              <div className="flex justify-center">
                <img src={pattern} alt="Pattern to identify" className="max-h-48" />
              </div>
            )}
          </div>
        </div>
        
        <div className="grid grid-cols-2 gap-3">
          {options.map((option, index) => (
            <Card 
              key={index}
              className={`cursor-pointer transition-all ${
                selectedOption === option 
                  ? 'ring-2 ring-blue-500 bg-blue-50' 
                  : 'hover:bg-gray-50'
              }`}
              onClick={() => handleOptionSelect(option)}
            >
              <CardContent className="p-4 text-center">
                {option}
              </CardContent>
            </Card>
          ))}
        </div>
        
        <div className="mt-4 flex justify-center">
          <Button 
            onClick={handleSubmit} 
            disabled={selectedOption === null || showFeedback}
            className="px-8"
          >
            Submit Answer
          </Button>
        </div>
        
        {showFeedback && (
          <div className={`mt-4 p-3 rounded-lg ${
            selectedOption === correctAnswer 
              ? 'bg-green-50 text-green-800 border border-green-200' 
              : 'bg-red-50 text-red-800 border border-red-200'
          }`}>
            <p className="font-medium">
              {selectedOption === correctAnswer 
                ? 'Correct! You identified the pattern.' 
                : `Incorrect. The correct pattern is "${correctAnswer}".`}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default PatternRecognition;
