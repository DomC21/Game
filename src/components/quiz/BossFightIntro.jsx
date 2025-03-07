import React from 'react';
import { Button } from '../ui-js/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '../ui-js/card';
import { Badge } from '../ui-js/badge';
import { Trophy, AlertTriangle } from 'lucide-react';

const BossFightIntro = ({ title, description, requiredScore, totalQuestions, onStart }) => {
  return (
    <Card className="border-red-200 max-w-2xl mx-auto">
      <CardHeader className="bg-gradient-to-r from-red-600 to-orange-600 text-white">
        <div className="flex items-center justify-between">
          <CardTitle className="text-2xl flex items-center">
            <Trophy className="mr-2 h-6 w-6" />
            {title}
          </CardTitle>
          <Badge className="bg-white/20 backdrop-blur-sm text-white">
            Boss Fight
          </Badge>
        </div>
        <CardDescription className="text-white/90">
          Test your mastery of this level's concepts
        </CardDescription>
      </CardHeader>
      <CardContent className="pt-6 space-y-6">
        <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
          <div className="flex items-start">
            <AlertTriangle className="h-5 w-5 text-orange-600 mr-2 mt-0.5" />
            <div>
              <p className="font-medium text-orange-800">Challenge Requirements</p>
              <p className="text-orange-700 text-sm">
                You need to score at least {requiredScore}% to pass this boss fight and unlock the next level.
              </p>
            </div>
          </div>
        </div>
        
        <div>
          <p className="text-gray-700">{description}</p>
        </div>
        
        <div className="grid grid-cols-2 gap-4 text-center">
          <div className="bg-gray-50 rounded-lg p-3">
            <p className="text-sm text-gray-500">Questions</p>
            <p className="font-bold text-xl">{totalQuestions}</p>
          </div>
          <div className="bg-gray-50 rounded-lg p-3">
            <p className="text-sm text-gray-500">Required Score</p>
            <p className="font-bold text-xl">{requiredScore}%</p>
          </div>
        </div>
      </CardContent>
      <CardFooter className="flex justify-center pt-2 pb-6">
        <Button onClick={onStart} className="px-8">
          Begin Challenge
        </Button>
      </CardFooter>
    </Card>
  );
};

export default BossFightIntro;
