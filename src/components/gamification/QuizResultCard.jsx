import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '../ui-js/card';
import { Button } from '../ui-js/button';
import { Progress } from '../ui-js/progress';
import { Badge } from '../ui-js/badge';

const QuizResultCard = ({ result, onContinue }) => {
  const [showCelebration, setShowCelebration] = useState(false);
  const { score, max_score, points_earned, level_up, new_level, new_achievements } = result;
  
  const scorePercentage = (score / max_score) * 100;
  const isPerfectScore = score === max_score;
  const isGoodScore = scorePercentage >= 70;
  
  useEffect(() => {
    // Show celebration animation after a short delay
    const timer = setTimeout(() => {
      setShowCelebration(true);
    }, 500);
    
    return () => clearTimeout(timer);
  }, []);
  
  return (
    <Card className="relative overflow-hidden">
      {/* Celebration effects */}
      {showCelebration && (isPerfectScore || level_up || new_achievements?.length > 0) && (
        <div className="absolute inset-0 pointer-events-none">
          <div className="absolute inset-0 bg-confetti opacity-10"></div>
          {Array.from({ length: 50 }).map((_, i) => (
            <div 
              key={i}
              className="absolute w-2 h-2 rounded-full animate-confetti"
              style={{
                backgroundColor: getRandomColor(),
                left: `${Math.random() * 100}%`,
                top: `-20px`,
                animationDelay: `${Math.random() * 3}s`,
                animationDuration: `${3 + Math.random() * 2}s`
              }}
            />
          ))}
        </div>
      )}
      
      <CardHeader className={`text-center ${isPerfectScore ? 'bg-green-50' : isGoodScore ? 'bg-blue-50' : 'bg-orange-50'}`}>
        <CardTitle className="text-2xl">
          {isPerfectScore ? '🎉 Perfect Score!' : isGoodScore ? '👏 Great Job!' : '👍 Good Effort!'}
        </CardTitle>
        <CardDescription>
          You scored {score} out of {max_score} points
        </CardDescription>
      </CardHeader>
      
      <CardContent className="space-y-6 pt-6">
        <div className="text-center">
          <div className={`inline-flex items-center justify-center w-24 h-24 rounded-full mb-4 ${
            isPerfectScore ? 'bg-green-100 text-green-700' : 
            isGoodScore ? 'bg-blue-100 text-blue-700' : 
            'bg-orange-100 text-orange-700'
          }`}>
            <span className="text-3xl font-bold">
              {Math.round(scorePercentage)}%
            </span>
          </div>
          <Progress 
            value={scorePercentage} 
            className={`h-2 w-full max-w-md mx-auto ${
              isPerfectScore ? 'bg-green-200' : 
              isGoodScore ? 'bg-blue-200' : 
              'bg-orange-200'
            }`} 
          />
        </div>

        <div className="space-y-4">
          <div className={`p-4 rounded-lg ${isPerfectScore ? 'bg-green-50' : 'bg-blue-50'} flex items-center justify-between animate-fadeIn`}>
            <span className="font-medium">Points Earned:</span>
            <Badge className="bg-blue-100 text-blue-800 text-lg px-3 py-1">
              +{points_earned} Points
            </Badge>
          </div>
          
          {level_up && (
            <div className="p-4 rounded-lg bg-purple-50 border border-purple-100 animate-bounceIn">
              <div className="flex items-center">
                <span className="text-2xl mr-2">🌟</span>
                <div>
                  <h3 className="font-bold text-purple-800">Level Up!</h3>
                  <p className="text-purple-700">
                    Congratulations! You've reached Level {new_level}
                  </p>
                </div>
              </div>
            </div>
          )}
          
          {new_achievements && new_achievements.length > 0 && (
            <div className="space-y-3 animate-fadeIn">
              <h3 className="font-medium text-gray-700">New Achievements Unlocked:</h3>
              {new_achievements.map((achievement, index) => (
                <div 
                  key={achievement.id} 
                  className="p-4 rounded-lg bg-yellow-50 border border-yellow-100"
                  style={{ animationDelay: `${0.3 * (index + 1)}s` }}
                >
                  <div className="flex items-center">
                    <span className="text-2xl mr-2">🏆</span>
                    <div>
                      <h3 className="font-bold text-yellow-800">{achievement.title}</h3>
                      <p className="text-yellow-700 text-sm">
                        {achievement.description}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </CardContent>
      
      <CardFooter className="flex justify-center pt-2 pb-6">
        <Button onClick={onContinue} className="px-8">
          Continue
        </Button>
      </CardFooter>
    </Card>
  );
};

// Helper function to get random colors for confetti
const getRandomColor = () => {
  const colors = [
    '#FCD34D', // yellow-300
    '#34D399', // green-400
    '#60A5FA', // blue-400
    '#F87171', // red-400
    '#A78BFA', // purple-400
    '#FBBF24', // amber-400
    '#EC4899', // pink-500
  ];
  
  return colors[Math.floor(Math.random() * colors.length)];
};

export default QuizResultCard;
