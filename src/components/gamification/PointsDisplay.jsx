import React from 'react';
import { Card, CardContent } from '../ui-js/card';
import { Badge } from '../ui-js/badge';

const PointsDisplay = ({ points, xp, className }) => {
  return (
    <Card className={`overflow-hidden ${className}`}>
      <div className="bg-gradient-to-r from-purple-600 to-indigo-600 p-4">
        <div className="flex justify-between items-center">
          <div className="flex items-center">
            <span className="text-yellow-300 text-xl mr-2">🏆</span>
            <h3 className="text-white font-bold text-lg">Your Points</h3>
          </div>
          <Badge className="bg-white/20 text-white backdrop-blur-sm">
            Total Score
          </Badge>
        </div>
      </div>
      <CardContent className="p-4">
        <div className="flex justify-between items-center">
          <div className="flex flex-col">
            <span className="text-3xl font-bold text-purple-700">{points}</span>
            <span className="text-sm text-gray-500">Total Points</span>
          </div>
          <div className="flex flex-col items-end">
            <span className="text-2xl font-bold text-indigo-600">{xp}</span>
            <span className="text-sm text-gray-500">Experience Points</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default PointsDisplay;
