import React, { useState } from 'react';
import { Button } from '../ui-js/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '../ui-js/card';
import { Badge } from '../ui-js/badge';

const ScenarioChallenge = ({ scenario, options, correctOption, explanation, onAnswer }) => {
  const [selectedOption, setSelectedOption] = useState(null);
  const [showFeedback, setShowFeedback] = useState(false);
  
  const handleOptionSelect = (option) => {
    setSelectedOption(option);
  };
  
  const handleSubmit = () => {
    setShowFeedback(true);
    onAnswer(selectedOption === correctOption);
  };
  
  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <CardTitle>Trading Scenario</CardTitle>
          <CardDescription>
            What would you do in this situation?
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
            <p>{scenario}</p>
          </div>
          
          <div className="space-y-3">
            {options.map((option, index) => (
              <div 
                key={index}
                className={`p-3 rounded-lg border cursor-pointer transition-all ${
                  selectedOption === option 
                    ? 'border-blue-500 bg-blue-50' 
                    : 'border-gray-200 hover:bg-gray-50'
                }`}
                onClick={() => handleOptionSelect(option)}
              >
                <p>{option}</p>
              </div>
            ))}
          </div>
        </CardContent>
        <CardFooter>
          <Button 
            onClick={handleSubmit} 
            disabled={selectedOption === null || showFeedback}
            className="w-full"
          >
            Submit Decision
          </Button>
        </CardFooter>
      </Card>
      
      {showFeedback && (
        <Card className={selectedOption === correctOption ? 'border-green-200' : 'border-red-200'}>
          <CardHeader className={selectedOption === correctOption ? 'bg-green-50' : 'bg-red-50'}>
            <div className="flex items-center justify-between">
              <CardTitle className={selectedOption === correctOption ? 'text-green-800' : 'text-red-800'}>
                {selectedOption === correctOption ? 'Good Decision!' : 'Not the Best Choice'}
              </CardTitle>
              <Badge className={selectedOption === correctOption ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}>
                {selectedOption === correctOption ? 'Correct' : 'Incorrect'}
              </Badge>
            </div>
          </CardHeader>
          <CardContent>
            <p className="text-gray-700">{explanation}</p>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default ScenarioChallenge;
