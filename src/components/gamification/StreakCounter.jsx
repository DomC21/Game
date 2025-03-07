import React from 'react';
import { Card, CardContent } from '../ui-js/card';

const StreakCounter = ({ streak, lastActivity }) => {
  // Calculate days since last activity
  const daysSinceLastActivity = lastActivity 
    ? Math.floor((new Date() - new Date(lastActivity)) / (1000 * 60 * 60 * 24)) 
    : null;
  
  // Determine if streak is at risk (no activity in the last day)
  const streakAtRisk = daysSinceLastActivity > 0;
  
  return (
    <Card className="overflow-hidden">
      <CardContent className="p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <span className="text-2xl mr-2">🔥</span>
            <div>
              <h3 className="font-bold text-gray-800">Daily Streak</h3>
              <p className="text-sm text-gray-500">
                {streakAtRisk 
                  ? 'Complete a quiz today to maintain your streak!' 
                  : "You've completed your activity for today!"}
              </p>
            </div>
          </div>
          <div className="flex flex-col items-center">
            <span className={`text-2xl font-bold ${streakAtRisk ? 'text-orange-500' : 'text-green-600'}`}>
              {streak}
            </span>
            <span className="text-xs text-gray-500">days</span>
          </div>
        </div>
        
        {/* Streak calendar */}
        <div className="mt-3 flex justify-between">
          {Array.from({ length: 7 }).map((_, index) => {
            // This is a simplified version - in a real app, you'd check actual days
            const isActive = index < streak % 7;
            return (
              <div key={index} className="flex flex-col items-center">
                <div 
                  className={`w-6 h-6 rounded-full flex items-center justify-center ${
                    isActive ? 'bg-green-100 text-green-600' : 'bg-gray-100 text-gray-400'
                  }`}
                >
                  {isActive ? '✓' : ''}
                </div>
                <span className="text-xs text-gray-500 mt-1">
                  {getDayLabel(index)}
                </span>
              </div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
};

// Helper function to get day label
const getDayLabel = (index) => {
  const days = ['M', 'T', 'W', 'T', 'F', 'S', 'S'];
  return days[index];
};

export default StreakCounter;
