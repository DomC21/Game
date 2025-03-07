import React, { useState, useEffect } from 'react';
import { Button } from '../ui-js/button';

const LevelUpNotification = ({ level, onClose }) => {
  const [isVisible, setIsVisible] = useState(false);
  
  useEffect(() => {
    // Show notification with animation
    setIsVisible(true);
    
    // Auto-hide after 7 seconds
    const timer = setTimeout(() => {
      setIsVisible(false);
      setTimeout(onClose, 500); // Call onClose after exit animation
    }, 7000);
    
    return () => clearTimeout(timer);
  }, [onClose]);
  
  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
      <div 
        className={`bg-white rounded-lg shadow-xl overflow-hidden max-w-md w-full transition-all duration-700 transform ${
          isVisible ? 'scale-100 opacity-100' : 'scale-90 opacity-0'
        }`}
      >
        <div className="bg-gradient-to-r from-blue-600 to-indigo-700 px-6 py-4 text-center">
          <h2 className="text-2xl font-bold text-white">Level Up!</h2>
        </div>
        
        <div className="p-6 text-center">
          <div className="w-24 h-24 rounded-full bg-blue-100 flex items-center justify-center mx-auto mb-4">
            <span className="text-4xl">🌟</span>
          </div>
          
          <h3 className="text-xl font-bold text-gray-900 mb-2">
            Congratulations!
          </h3>
          
          <p className="text-gray-600 mb-6">
            You've reached <span className="font-bold text-blue-600">Level {level}</span>!
            Keep up the great work and unlock more content.
          </p>
          
          <div className="flex justify-center space-x-4">
            <Button
              onClick={() => {
                setIsVisible(false);
                setTimeout(onClose, 500);
              }}
              className="px-6"
            >
              Continue
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LevelUpNotification;
