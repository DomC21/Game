import React from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui-js/card';
import { Progress } from '../ui-js/progress';
import { Badge } from '../ui-js/badge';

const LevelProgressCard = ({ currentLevel, nextLevel, experiencePoints, totalPoints }) => {
  // Calculate progress percentage for next level
  const progressPercentage = nextLevel 
    ? Math.min(100, (experiencePoints / nextLevel.required_points) * 100)
    : 100;
  
  return (
    <Card className="overflow-hidden">
      <div className="bg-gradient-to-r from-blue-600 to-indigo-700 px-6 py-4">
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-xl font-bold text-white">Level {currentLevel}</h2>
            <p className="text-blue-100">
              {nextLevel 
                ? `${nextLevel.required_points - experiencePoints} XP to Level ${nextLevel.level_number}` 
                : 'Maximum level reached!'}
            </p>
          </div>
          <div className="bg-white/20 backdrop-blur-sm rounded-lg px-4 py-2 flex items-center">
            <span className="text-yellow-300 mr-2">🏆</span>
            <span className="font-bold text-white">{totalPoints} Points</span>
          </div>
        </div>
      </div>
      <CardContent className="pt-6">
        <div className="space-y-4">
          <div>
            <div className="flex justify-between mb-2">
              <span className="font-medium">Progress to Level {nextLevel?.level_number || (currentLevel + 1)}</span>
              <span className="text-sm text-gray-500">
                {experiencePoints} / {nextLevel?.required_points || experiencePoints} XP
              </span>
            </div>
            <Progress value={progressPercentage} className="h-2" />
          </div>
          
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <span className="text-blue-600 mr-2">📚</span>
              <span className="text-sm text-gray-600">Keep learning to earn more points!</span>
            </div>
            <Badge className="bg-blue-100 text-blue-800">
              {getLevelTitle(currentLevel)}
            </Badge>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

// Helper function to get a title based on level
const getLevelTitle = (level) => {
  const titles = [
    'Beginner',
    'Novice',
    'Apprentice',
    'Intermediate',
    'Advanced',
    'Expert',
    'Master',
    'Grandmaster',
    'Legend'
  ];
  
  if (level <= 0) return titles[0];
  if (level > titles.length) return titles[titles.length - 1];
  return titles[level - 1];
};

export default LevelProgressCard;
