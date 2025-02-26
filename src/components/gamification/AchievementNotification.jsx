import React, { useState, useEffect } from 'react';

const AchievementNotification = ({ achievement, onClose }) => {
  const [isVisible, setIsVisible] = useState(false);
  
  useEffect(() => {
    // Show notification with animation
    setIsVisible(true);
    
    // Auto-hide after 5 seconds
    const timer = setTimeout(() => {
      setIsVisible(false);
      setTimeout(onClose, 500); // Call onClose after exit animation
    }, 5000);
    
    return () => clearTimeout(timer);
  }, [onClose]);
  
  return (
    <div 
      className={`fixed bottom-4 right-4 max-w-sm bg-white rounded-lg shadow-lg border border-yellow-200 transition-all duration-500 transform ${
        isVisible ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'
      }`}
    >
      <div className="p-4">
        <div className="flex items-center">
          <div className="flex-shrink-0 bg-yellow-100 rounded-full p-2">
            <span className="text-2xl">🏆</span>
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-gray-900">Achievement Unlocked!</h3>
            <div className="mt-1 text-sm text-gray-500">
              <p className="font-medium">{achievement.title}</p>
              <p>{achievement.description}</p>
            </div>
          </div>
        </div>
        <div className="mt-2 flex justify-between items-center">
          <span className="text-xs text-green-600 font-medium">+{achievement.points} Points</span>
          <button
            type="button"
            className="text-sm text-gray-400 hover:text-gray-500"
            onClick={() => {
              setIsVisible(false);
              setTimeout(onClose, 500);
            }}
          >
            Dismiss
          </button>
        </div>
      </div>
    </div>
  );
};

export default AchievementNotification;
