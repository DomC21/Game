import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui-js/card';
import { Badge } from '../ui-js/badge';

const AchievementCard = ({ achievement, showDetails = false }) => {
  const { title, description, earned, points, category } = achievement;
  
  return (
    <Card className={`transition-all duration-300 ${earned ? 'bg-white border-green-200' : 'bg-gray-50 border-gray-200'}`}>
      <CardHeader className={`pb-2 ${earned ? 'bg-green-50' : ''}`}>
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg flex items-center">
            {getAchievementIcon(category, earned)}
            <span className="ml-2">{title}</span>
          </CardTitle>
          {earned && (
            <Badge className="bg-green-100 text-green-800 hover:bg-green-200">
              +{points} Points
            </Badge>
          )}
        </div>
      </CardHeader>
      <CardContent className="pt-3">
        <p className="text-sm text-gray-600 mb-3">{description}</p>
        <div className="flex justify-between items-center">
          <Badge variant={earned ? 'default' : 'outline'} className={earned ? 'bg-green-100 text-green-800 hover:bg-green-200' : ''}>
            {earned ? 'Earned' : 'Not Earned Yet'}
          </Badge>
          
          {showDetails && earned && (
            <span className="text-xs text-gray-500">
              Earned on {new Date(achievement.earned_at).toLocaleDateString()}
            </span>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

// Helper function to get the appropriate icon based on achievement category
const getAchievementIcon = (category, earned) => {
  const baseClass = "h-5 w-5 mr-1";
  const colorClass = earned ? "text-yellow-500" : "text-gray-400";
  
  return (
    <span className={`${baseClass} ${colorClass}`}>
      {getCategoryEmoji(category)}
    </span>
  );
};

// Helper function to get emoji based on category
const getCategoryEmoji = (category) => {
  switch (category?.toLowerCase()) {
    case 'quiz':
      return '🎯';
    case 'streak':
      return '🔥';
    case 'completion':
      return '🏆';
    case 'mastery':
      return '⭐';
    case 'special':
      return '✨';
    default:
      return '🏅';
  }
};

export default AchievementCard;
