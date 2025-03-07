import React, { createContext, useState, useContext, useEffect } from 'react';
import { useAuth } from './AuthContext';
import { progressAPI, leaderboardAPI } from '../services/api';
import AchievementNotification from '../components/gamification/AchievementNotification';
import LevelUpNotification from '../components/gamification/LevelUpNotification';

const GamificationContext = createContext();

export const useGamification = () => useContext(GamificationContext);

export const GamificationProvider = ({ children }) => {
  const { token, currentUser, refreshUser } = useAuth();
  const [achievements, setAchievements] = useState([]);
  const [leaderboard, setLeaderboard] = useState([]);
  const [quizAttempts, setQuizAttempts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Notification states
  const [newAchievement, setNewAchievement] = useState(null);
  const [levelUp, setLevelUp] = useState(null);
  
  // Fetch gamification data
  const fetchGamificationData = async () => {
    if (!token) return;
    
    try {
      setLoading(true);
      
      // Mock achievements data
      const mockAchievements = [
        {
          id: 1,
          title: "First Steps",
          description: "Complete your first quiz",
          badge_image: "badge-first-steps.png",
          requirement_type: "quiz_completion",
          requirement_value: 1,
          earned: true
        },
        {
          id: 2,
          title: "Knowledge Seeker",
          description: "Read 5 chapters",
          badge_image: "badge-knowledge-seeker.png",
          requirement_type: "chapters_read",
          requirement_value: 5,
          earned: true
        },
        {
          id: 3,
          title: "Quiz Master",
          description: "Score 100% on any quiz",
          badge_image: "badge-quiz-master.png",
          requirement_type: "perfect_score",
          requirement_value: 1,
          earned: false
        },
        {
          id: 4,
          title: "Dedicated Learner",
          description: "Log in for 5 consecutive days",
          badge_image: "badge-dedicated-learner.png",
          requirement_type: "login_streak",
          requirement_value: 5,
          earned: false
        },
        {
          id: 5,
          title: "Level 1 Master",
          description: "Complete all chapters in Level 1",
          badge_image: "badge-level-1-master.png",
          requirement_type: "level_completion",
          requirement_value: 1,
          earned: true
        }
      ];
      setAchievements(mockAchievements);
      
      // Mock leaderboard data
      const mockLeaderboard = [
        { id: 1, username: "investor123", total_points: 850 },
        { id: 2, username: "tradingpro", total_points: 720 },
        { id: 3, username: "stockmaster", total_points: 680 },
        { id: 4, username: "learner456", total_points: 550 },
        { id: 5, username: currentUser?.username || "user", total_points: currentUser?.total_points || 500 },
        { id: 6, username: "newtrader", total_points: 320 },
        { id: 7, username: "investingfan", total_points: 280 },
        { id: 8, username: "marketwatcher", total_points: 220 },
        { id: 9, username: "cryptofan", total_points: 180 },
        { id: 10, username: "beginner101", total_points: 120 }
      ];
      setLeaderboard(mockLeaderboard);
      
      // Mock quiz attempts data
      const mockQuizAttempts = [
        {
          id: 1,
          quiz_id: 1,
          score: 8,
          max_score: 10,
          points_earned: 40,
          completed_at: new Date(Date.now() - 86400000 * 2).toISOString() // 2 days ago
        },
        {
          id: 2,
          quiz_id: 2,
          score: 7,
          max_score: 10,
          points_earned: 35,
          completed_at: new Date(Date.now() - 86400000 * 1).toISOString() // 1 day ago
        },
        {
          id: 3,
          quiz_id: 3,
          score: 9,
          max_score: 10,
          points_earned: 45,
          completed_at: new Date().toISOString() // today
        }
      ];
      setQuizAttempts(mockQuizAttempts);
      
      setError(null);
    } catch (err) {
      console.error('Error fetching gamification data:', err);
      setError('Failed to load gamification data. Please try again.');
    } finally {
      setLoading(false);
    }
  };
  
  // Check for new achievements and level ups
  useEffect(() => {
    if (currentUser && currentUser.recent_achievements && currentUser.recent_achievements.length > 0) {
      // Show the most recent achievement notification
      setNewAchievement(currentUser.recent_achievements[0]);
    }
    
    if (currentUser && currentUser.recent_level_up) {
      setLevelUp(currentUser.current_level);
    }
  }, [currentUser]);
  
  // Fetch data when token changes
  useEffect(() => {
    if (token) {
      fetchGamificationData();
    }
  }, [token]);
  
  // Refresh data
  const refreshGamificationData = () => {
    fetchGamificationData();
    refreshUser();
  };
  
  // Handle achievement notification close
  const handleAchievementNotificationClose = () => {
    setNewAchievement(null);
  };
  
  // Handle level up notification close
  const handleLevelUpNotificationClose = () => {
    setLevelUp(null);
  };
  
  const value = {
    achievements,
    leaderboard,
    quizAttempts,
    loading,
    error,
    refreshGamificationData,
  };
  
  return (
    <GamificationContext.Provider value={value}>
      {children}
      
      {/* Achievement notification */}
      {newAchievement && (
        <AchievementNotification 
          achievement={newAchievement} 
          onClose={handleAchievementNotificationClose} 
        />
      )}
      
      {/* Level up notification */}
      {levelUp && (
        <LevelUpNotification 
          level={levelUp} 
          onClose={handleLevelUpNotificationClose} 
        />
      )}
    </GamificationContext.Provider>
  );
};
