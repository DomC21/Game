import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useGamification } from '../contexts/GamificationContext';
import { contentAPI, progressAPI, leaderboardAPI } from '../services/api';
import { Button } from '../components/ui-js/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '../components/ui-js/card';
import { Progress } from '../components/ui-js/progress';
import { Badge } from '../components/ui-js/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui-js/tabs';

// Gamification components
import LevelProgressCard from '../components/gamification/LevelProgressCard';
import AchievementCard from '../components/gamification/AchievementCard';
import LeaderboardCard from '../components/gamification/LeaderboardCard';
import PointsDisplay from '../components/gamification/PointsDisplay';
import StreakCounter from '../components/gamification/StreakCounter';
import BadgeCollection from '../components/gamification/BadgeCollection';
import LearningPathMap from '../components/gamification/LearningPathMap';
import QuizHistoryCard from '../components/gamification/QuizHistoryCard';
import StatsSummary from '../components/gamification/StatsSummary';
import ProgressChart from '../components/gamification/ProgressChart';

const Dashboard = () => {
  const { currentUser, token, logout } = useAuth();
  const { 
    achievements, 
    leaderboard, 
    quizAttempts, 
    loading: gamificationLoading, 
    error: gamificationError,
    refreshGamificationData
  } = useGamification();
  
  const navigate = useNavigate();
  const [levels, setLevels] = useState([]);
  const [userStreak, setUserStreak] = useState({ streak: 0, last_activity: null });
  const [progressHistory, setProgressHistory] = useState([]);
  const [userStats, setUserStats] = useState(null);
  const [nextLevelRequirements, setNextLevelRequirements] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('levels');

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setIsLoading(true);
        
        if (!token) {
          navigate('/login');
          return;
        }
        
        // Fetch levels
        try {
          const levelsData = await contentAPI.getLevels();
          setLevels(levelsData);
        } catch (err) {
          console.error('Error fetching levels:', err);
          // Set empty levels array as fallback
          setLevels([]);
        }
        
        // Fetch user streak data
        try {
          const streakData = await progressAPI.getUserProgress();
          if (streakData && streakData.streak) {
            setUserStreak(streakData.streak);
          } else {
            // Fallback to mock data if API call fails
            setUserStreak({ 
              streak: 3, 
              last_activity: new Date().toISOString() 
            });
          }
        } catch (err) {
          console.error('Error fetching user streak:', err);
          // Fallback to mock data
          setUserStreak({ 
            streak: 3, 
            last_activity: new Date().toISOString() 
          });
        }
        
        // Set next level requirements based on current user level
        setNextLevelRequirements({
          level_number: currentUser.current_level + 1,
          required_points: 100 * (currentUser.current_level + 1),
          title: `Level ${currentUser.current_level + 1}`,
          description: `Advanced trading concepts and strategies`
        });
        
        // Fetch user stats or use fallback
        try {
          const statsData = await progressAPI.getUserProgress();
          if (statsData && statsData.stats) {
            setUserStats(statsData.stats);
          } else {
            // Fallback to mock data
            setUserStats({
              quizzes_completed: 5,
              chapters_read: 8,
              correct_answers: 25,
              total_questions: 30,
              accuracy: 83
            });
          }
        } catch (err) {
          console.error('Error fetching user stats:', err);
          // Fallback to mock data
          setUserStats({
            quizzes_completed: 5,
            chapters_read: 8,
            correct_answers: 25,
            total_questions: 30,
            accuracy: 83
          });
        }
        
        // Generate progress history data
        const today = new Date();
        const mockHistory = [];
        for (let i = 6; i >= 0; i--) {
          const date = new Date(today);
          date.setDate(date.getDate() - i);
          mockHistory.push({
            date: date.toISOString(),
            points_earned: Math.floor(Math.random() * 50) + 10
          });
        }
        setProgressHistory(mockHistory);
        
        // Refresh gamification data
        refreshGamificationData();
        
      } catch (err) {
        console.error('Error fetching dashboard data:', err);
        setError('Failed to load dashboard data. Please try again.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchDashboardData();
  }, [token, navigate, refreshGamificationData]);

  const handleTabChange = (value) => {
    setActiveTab(value);
  };

  if (isLoading || gamificationLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading your learning dashboard...</p>
        </div>
      </div>
    );
  }

  if (error || gamificationError) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen p-4">
        <p className="text-red-500 mb-2">{error || gamificationError}</p>
        <Button onClick={() => window.location.reload()} className="mt-4">
          Try Again
        </Button>
      </div>
    );
  }

  if (!currentUser) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen p-4">
        <p className="text-gray-600 mb-2">Your session has expired. Please log in again.</p>
        <Button onClick={() => navigate('/login')} className="mt-4">
          Log In
        </Button>
      </div>
    );
  }

  // Calculate progress percentage for next level
  const currentLevel = currentUser.current_level;
  const nextLevel = levels.find(level => level.level_number === currentLevel + 1);
  const progressPercentage = nextLevel 
    ? Math.min(100, (currentUser.experience_points / nextLevel.required_points) * 100)
    : 100;

  // Filter earned achievements
  const earnedAchievements = achievements.filter(achievement => achievement.earned);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">Trading &amp; Investing eBook</h1>
          <Button variant="ghost" onClick={logout} className="flex items-center">
            Sign Out
          </Button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        {/* User Profile Summary */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="md:col-span-2">
            <LevelProgressCard 
              currentLevel={currentUser.current_level}
              nextLevel={nextLevelRequirements}
              experiencePoints={currentUser.experience_points}
              totalPoints={currentUser.total_points}
            />
          </div>
          
          <div>
            <StreakCounter 
              streak={userStreak.streak} 
              lastActivity={userStreak.last_activity} 
            />
          </div>
        </div>
        
        {/* Welcome Message and Stats */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="text-xl">Welcome, {currentUser.username}!</CardTitle>
            <CardDescription>Continue your learning journey</CardDescription>
          </CardHeader>
          <CardContent>
            {userStats && (
              <StatsSummary stats={userStats} />
            )}
          </CardContent>
        </Card>

        {/* Main Content */}
        <Tabs value={activeTab} onValueChange={handleTabChange}>
          <TabsList className="mb-6 bg-white p-1 rounded-lg shadow-sm">
            <TabsTrigger value="levels" className="flex items-center">
              Levels &amp; Chapters
            </TabsTrigger>
            <TabsTrigger value="achievements" className="flex items-center">
              Achievements
            </TabsTrigger>
            <TabsTrigger value="progress" className="flex items-center">
              Progress
            </TabsTrigger>
            <TabsTrigger value="profile" className="flex items-center">
              Profile
            </TabsTrigger>
          </TabsList>
        
        {/* Levels Tab */}
        <TabsContent value="levels" className="space-y-6">
          <div className="grid grid-cols-1 gap-6">
            {levels.map(level => (
              <Card key={level.id} className={level.is_locked ? 'border-gray-200' : 'border-blue-200'}>
                <CardHeader className={level.is_locked ? '' : 'bg-blue-50'}>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center">
                      <div className={`flex items-center justify-center rounded-full w-10 h-10 mr-4 ${level.is_locked ? 'bg-gray-100 text-gray-500' : 'bg-blue-100 text-blue-700'}`}>
                        <span className="font-bold">{level.level_number}</span>
                      </div>
                      <div>
                        <CardTitle className="text-xl">
                          {level.title}
                          {level.is_locked && (
                            <Badge variant="outline" className="ml-2 bg-gray-100">
                              Locked
                            </Badge>
                          )}
                        </CardTitle>
                        <CardDescription>{level.description}</CardDescription>
                      </div>
                    </div>
                    <div>
                      {level.is_locked ? (
                        <div className="text-sm text-gray-500 flex items-center">
                          <span>Requires {level.required_points} Points</span>
                        </div>
                      ) : (
                        <Link to={`/levels/${level.id}`}>
                          <Button className="flex items-center">
                            Start Learning
                          </Button>
                        </Link>
                      )}
                    </div>
                  </div>
                </CardHeader>
                {level.chapters && level.chapters.length > 0 && !level.is_locked && (
                  <CardContent>
                    <h3 className="font-medium text-gray-700 mb-3">Chapters:</h3>
                    <ul className="space-y-2">
                      {level.chapters.map((chapter, index) => (
                        <li key={chapter.id} className="flex items-center justify-between p-3 rounded-lg bg-gray-50 hover:bg-gray-100">
                          <div className="flex items-center">
                            <span className="bg-gray-200 text-gray-700 rounded-full w-6 h-6 flex items-center justify-center mr-3 text-sm">
                              {index + 1}
                            </span>
                            <span>{chapter.title}</span>
                          </div>
                          <Link to={`/chapters/${chapter.id}`}>
                            <Button variant="outline" size="sm">
                              Read
                            </Button>
                          </Link>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                )}
              </Card>
            ))}
          </div>
        </TabsContent>
        
        {/* Achievements Tab */}
        <TabsContent value="achievements" className="space-y-6">
          <div className="grid grid-cols-1 gap-6">
            <BadgeCollection badges={achievements} className="mb-6" />
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {achievements.map(achievement => (
                <AchievementCard 
                  key={achievement.id} 
                  achievement={achievement} 
                  showDetails={true}
                />
              ))}
            </div>
          </div>
        </TabsContent>
        
        {/* Progress Tab */}
        <TabsContent value="progress" className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Progress Chart */}
            <ProgressChart 
              progressData={progressHistory.map(item => ({
                label: new Date(item.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
                value: item.points_earned
              }))} 
              className="md:col-span-2"
            />
            
            {/* Quiz History */}
            <QuizHistoryCard quizAttempts={quizAttempts} />
            
            {/* Leaderboard */}
            <LeaderboardCard 
              leaderboard={leaderboard} 
              currentUserId={currentUser.id} 
            />
          </div>
          
          {/* Learning Path */}
          <LearningPathMap 
            levels={levels} 
            currentLevel={currentUser.current_level} 
          />
        </TabsContent>
        
        {/* Profile Tab */}
        <TabsContent value="profile">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card className="md:col-span-2">
              <CardHeader>
                <CardTitle>Your Profile</CardTitle>
                <CardDescription>Your account information and learning statistics</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <h3 className="font-medium text-gray-700">Account Information</h3>
                    <div className="grid grid-cols-1 gap-4">
                      <div className="bg-gray-50 p-4 rounded-lg">
                        <p className="text-sm font-medium text-gray-500">Username</p>
                        <p className="font-medium">{currentUser.username}</p>
                      </div>
                      <div className="bg-gray-50 p-4 rounded-lg">
                        <p className="text-sm font-medium text-gray-500">Email</p>
                        <p className="font-medium">{currentUser.email}</p>
                      </div>
                      <div className="bg-gray-50 p-4 rounded-lg">
                        <p className="text-sm font-medium text-gray-500">Member Since</p>
                        <p className="font-medium">{new Date(currentUser.created_at).toLocaleDateString()}</p>
                      </div>
                    </div>
                  </div>
                  
                  <div className="space-y-4">
                    <h3 className="font-medium text-gray-700">Learning Journey</h3>
                    <div className="grid grid-cols-1 gap-4">
                      <div className="bg-blue-50 p-4 rounded-lg border border-blue-100">
                        <p className="text-sm font-medium text-blue-700">Current Level</p>
                        <p className="font-medium text-2xl">{currentUser.current_level}</p>
                      </div>
                      <div className="bg-yellow-50 p-4 rounded-lg border border-yellow-100">
                        <p className="text-sm font-medium text-yellow-700">Achievements Earned</p>
                        <p className="font-medium text-2xl">
                          {achievements.filter(a => a.earned).length} / {achievements.length}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div className="pt-4 border-t border-gray-200">
                  <Button variant="outline" onClick={logout} className="w-full">
                    Sign Out
                  </Button>
                </div>
              </CardContent>
            </Card>
            
            <div className="space-y-6">
              <PointsDisplay 
                points={currentUser.total_points} 
                xp={currentUser.experience_points} 
              />
              
              <Card>
                <CardHeader>
                  <CardTitle className="text-sm">Quick Links</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <Button variant="outline" className="w-full justify-start" onClick={() => setActiveTab('levels')}>
                      View Levels
                    </Button>
                    <Button variant="outline" className="w-full justify-start" onClick={() => setActiveTab('achievements')}>
                      View Achievements
                    </Button>
                    <Button variant="outline" className="w-full justify-start" onClick={() => setActiveTab('progress')}>
                      View Progress
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </TabsContent>
      </Tabs>
      </main>
    </div>
  );
};

export default Dashboard;
