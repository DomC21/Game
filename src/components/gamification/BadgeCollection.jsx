import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui-js/card';
import { Badge } from '../ui-js/badge';

const BadgeCollection = ({ badges, className }) => {
  // Group badges by category
  const groupedBadges = badges.reduce((acc, badge) => {
    const category = badge.category || 'Other';
    if (!acc[category]) {
      acc[category] = [];
    }
    acc[category].push(badge);
    return acc;
  }, {});
  
  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle className="flex items-center">
          <span className="text-yellow-500 mr-2">🏅</span>
          Your Badge Collection
        </CardTitle>
      </CardHeader>
      <CardContent>
        {Object.keys(groupedBadges).length > 0 ? (
          <div className="space-y-6">
            {Object.entries(groupedBadges).map(([category, categoryBadges]) => (
              <div key={category}>
                <h3 className="text-sm font-medium text-gray-500 mb-3">{category}</h3>
                <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
                  {categoryBadges.map((badge) => (
                    <BadgeItem key={badge.id} badge={badge} />
                  ))}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8">
            <p className="text-gray-500">Complete quizzes and challenges to earn badges!</p>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

const BadgeItem = ({ badge }) => {
  const { title, description, earned, icon } = badge;
  
  return (
    <div 
      className={`flex flex-col items-center p-3 rounded-lg border ${
        earned ? 'border-green-200 bg-green-50' : 'border-gray-200 bg-gray-50 opacity-60'
      }`}
    >
      <div 
        className={`w-12 h-12 rounded-full flex items-center justify-center mb-2 ${
          earned ? 'bg-green-100 text-green-600' : 'bg-gray-200 text-gray-400'
        }`}
      >
        <span className="text-xl">{icon || getBadgeIcon(badge.category)}</span>
      </div>
      <h4 className="text-sm font-medium text-center">{title}</h4>
      <Badge 
        className={`mt-2 text-xs ${
          earned ? 'bg-green-100 text-green-800' : 'bg-gray-200 text-gray-600'
        }`}
      >
        {earned ? 'Earned' : 'Locked'}
      </Badge>
    </div>
  );
};

// Helper function to get badge icon based on category
const getBadgeIcon = (category) => {
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

export default BadgeCollection;
