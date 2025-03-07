import React from 'react';
import { Card, CardContent } from '../ui-js/card';

const StatsSummary = ({ stats }) => {
  const { 
    total_points, 
    quizzes_completed, 
    quizzes_passed, 
    achievements_earned,
    current_streak,
    highest_streak,
    average_score,
    chapters_read
  } = stats;
  
  const statItems = [
    { label: 'Total Points', value: total_points, icon: '🏆' },
    { label: 'Quizzes Completed', value: quizzes_completed, icon: '📝' },
    { label: 'Quizzes Passed', value: quizzes_passed, icon: '✅' },
    { label: 'Achievements Earned', value: achievements_earned, icon: '🏅' },
    { label: 'Current Streak', value: current_streak, icon: '🔥' },
    { label: 'Highest Streak', value: highest_streak, icon: '⚡' },
    { label: 'Average Score', value: `${average_score}%`, icon: '📊' },
    { label: 'Chapters Read', value: chapters_read, icon: '📚' }
  ];
  
  return (
    <Card>
      <CardContent className="p-6">
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          {statItems.map((item, index) => (
            <StatItem key={index} {...item} />
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

const StatItem = ({ label, value, icon }) => {
  return (
    <div className="flex flex-col items-center text-center p-3 bg-gray-50 rounded-lg">
      <span className="text-2xl mb-2">{icon}</span>
      <span className="text-2xl font-bold text-gray-800">{value}</span>
      <span className="text-xs text-gray-500 mt-1">{label}</span>
    </div>
  );
};

export default StatsSummary;
