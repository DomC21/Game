import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui-js/card';

const ProgressChart = ({ progressData, className }) => {
  // This is a simplified version - in a real app, you'd use a charting library
  const maxValue = Math.max(...progressData.map(item => item.value));
  
  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle className="flex items-center">
          <span className="text-blue-500 mr-2">📈</span>
          Learning Progress
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-64 flex items-end space-x-2">
          {progressData.map((item, index) => {
            const heightPercentage = (item.value / maxValue) * 100;
            
            return (
              <div key={index} className="flex-1 flex flex-col items-center">
                <div className="w-full flex justify-center mb-2">
                  <div 
                    className="bg-blue-500 rounded-t-md w-full" 
                    style={{ height: `${heightPercentage}%` }}
                  ></div>
                </div>
                <div className="text-xs text-gray-500 truncate w-full text-center">
                  {item.label}
                </div>
              </div>
            );
          })}
        </div>
        
        <div className="mt-4 text-sm text-gray-500 text-center">
          Progress over time (last 7 days)
        </div>
      </CardContent>
    </Card>
  );
};

export default ProgressChart;
