import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui-js/card';
import { Badge } from '../ui-js/badge';
import { ChevronRight } from 'lucide-react';

const LearningPathMap = ({ levels, currentLevel }) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center">
          <span className="text-blue-500 mr-2">🗺️</span>
          Learning Path
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="relative">
          {/* Path line */}
          <div className="absolute left-6 top-0 bottom-0 w-1 bg-gray-200 z-0"></div>
          
          {/* Levels */}
          <div className="space-y-8 relative z-10">
            {levels.map((level) => {
              const isCurrentLevel = level.level_number === currentLevel;
              const isCompleted = level.level_number < currentLevel;
              const isLocked = level.level_number > currentLevel;
              
              return (
                <div key={level.id} className="flex items-start">
                  {/* Level indicator */}
                  <div 
                    className={`w-12 h-12 rounded-full flex items-center justify-center mr-4 z-10 ${
                      isCurrentLevel 
                        ? 'bg-blue-100 text-blue-600 border-2 border-blue-500' 
                        : isCompleted 
                          ? 'bg-green-100 text-green-600' 
                          : 'bg-gray-100 text-gray-400'
                    }`}
                  >
                    {isCompleted ? (
                      <span className="text-green-600">✓</span>
                    ) : (
                      <span>{level.level_number}</span>
                    )}
                  </div>
                  
                  {/* Level content */}
                  <div className={`flex-1 ${isLocked ? 'opacity-60' : ''}`}>
                    <div className="flex items-center">
                      <h3 className="font-bold text-gray-800">
                        Level {level.level_number}: {level.title}
                      </h3>
                      {isCurrentLevel && (
                        <Badge className="ml-2 bg-blue-100 text-blue-800">Current</Badge>
                      )}
                      {isLocked && (
                        <Badge className="ml-2 bg-gray-100 text-gray-600">
                          <span className="mr-1">🔒</span> Locked
                        </Badge>
                      )}
                    </div>
                    <p className="text-sm text-gray-600 mt-1">{level.description}</p>
                    
                    {/* Chapters preview */}
                    {level.chapters && level.chapters.length > 0 && !isLocked && (
                      <div className="mt-3 space-y-2">
                        {level.chapters.slice(0, 3).map((chapter) => (
                          <div 
                            key={chapter.id} 
                            className="flex items-center text-sm bg-gray-50 p-2 rounded-md"
                          >
                            <ChevronRight className="h-4 w-4 text-gray-400 mr-1" />
                            <span>{chapter.title}</span>
                          </div>
                        ))}
                        {level.chapters.length > 3 && (
                          <div className="text-xs text-gray-500 pl-6">
                            +{level.chapters.length - 3} more chapters
                          </div>
                        )}
                      </div>
                    )}
                    
                    {/* XP required */}
                    {isLocked && (
                      <div className="mt-2 text-sm text-gray-500">
                        <span className="font-medium">Required XP:</span> {level.required_points}
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default LearningPathMap;
